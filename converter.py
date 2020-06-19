from PIL import Image

bpp = {1: 2, 2: 4, 4: 16, 8: 256}
col = {2: 1, 4: 2, 16: 4, 256: 8}

def load_file(file):
    img = Image.open(file)
    pix = img.load()

    return pix, img.size[0], img.size[1]

def adjust_data(data: list):
    amount = min(data)

    copy = []
    for item in data:
        copy.append(item - amount)

    return copy

def convert_file_to_palette(file, b=8):
    img = Image.open(file)
    pix = img.load()

    return convert_image_to_palette(pix, 0, 0, img.size[0], img.size[1], b=b)

def convert_image_to_palette(pix, u, v, w, h, b=8):
    palette = [[]]

    counter = 0

    for y in range(v, v + h):
        for x in range(u, u + w):
            if not pix[x, y] in palette[-1]:
                palette[-1].append(pix[x, y])
                counter += 1
                if counter >= bpp[b]:
                    counter = 0
                    palette.append([])
    try:
        palette.remove([])
    except ValueError:
        pass  #just don't remove it. easy.

    return palette


def convert_file_to_data(file, u, v, w, h, palette: list, adjust=True):
    img = Image.open(file)
    pix = img.load()

    return convert_image_to_data(pix, u, v, w, h, palette, adjust=adjust)


def convert_file_simple(file, palette, adjust=True):
    img = Image.open(file)
    pix = img.load()

    return convert_image_to_data(pix, 0, 0, img.size[0], img.size[1], palette, adjust=adjust)


def convert_image_to_data(pix, u, v, w, h, palette: list, adjust=True):
    data = []

    # find specific palette index for conversion
    image_pal = convert_image_to_palette(pix, u, v, w, h)[0]  #only one
    pal_offset = 0
    pal_id = 0
    for pal in palette:
        if set(image_pal) == set(pal):
            pal_id = palette.index(pal)
            pal_offset = pal_id * len(pal)

    for y in range(v, v + h):
        for x in range(u, u + w):
            if adjust:
                data.append(palette[pal_id].index(pix[x, y]))
            else:
                data.append(pal_offset + palette[pal_id].index(pix[x, y]))

    return data


def convert_data_to_db(data, compress):
    """
    Converts data in list, uncompressed form,
    to db string data to be used in compiler.

    :param data: list of data to convert
    :param compress: how many bits each value is expected to have
    :return:
    """

    data_string = ".db "

    db_width = 64 / compress
    compress_count = 0
    pixels = 0

    for db_count, pixel in enumerate(data):

        compress_count += compress
        pixels |= pixel << (8 - compress_count)
        compress_count %= 8
        if compress_count == 0:
            data_string += "$" + format(pixels, '02x')
            pixels = 0

            if db_count < len(data) - 1:
                if not (db_count + 1) % db_width:
                    data_string += "\n.db "
                else:
                    data_string += ", "

    data_string += "\n"

    return data_string

def convert_lists_to_db(data, bpp):
    """
    Converts a list of lists into data.

    :param data: list of lists to convert
    :return: data converted to db string
    """

    converted_data = ""
    for sub_list in data:
        converted_data += (convert_data_to_db(sub_list, bpp))

    return converted_data

# conv_pal = convert_file_to_palette("images/tpal.png", 2)
# print(conv_pal)

# conv_data = convert_file_to_data("images/ttile.png", 0, 0, 12, 12, conv_pal)
# print(conv_data)
