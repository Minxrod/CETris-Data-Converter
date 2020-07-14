from PIL import Image, ImageDraw

db_size = {1: ".db ", 2: ".dw ", 3: ".dl "}

class Data:

    def __init__(self):
        self.data = []
        self.label = None
        self.other = None

        self.size = [1, 2, 1, 1, 3, 1, 1]
        self.name = ["t", "x", "y", "a", "ptr", "w", "h"]

    def convert_db(self):
        result = self.label
        for s, n in zip(self.size, self.data):
            result += db_size[s] + str(n) + "\n"

        # if self.other is not None:
        #     result += "\n" + self.data[4] + ":\n" + self.other.convert_db()

        return result

    def get_names(self):
        names = self.name

        if self.other is not None:
            names.extend(self.other.get_names())

        return names

    def get_data(self):
        data = self.data

        if self.other is not None:
            data.extend(self.other.get_data())

        return data

    def draw(self, image):
        pass

class Number(Data):

    def __init__(self):
        super().__init__()

        self.data = ["typeNumber", 0, 0, 32, "numberPtr", 3, 0]
        self.name = ["t", "x", "y", "color", "pointer", "digits", "bg color"]

    def draw(self, image):
        x = int(self.data[1])
        y = int(self.data[2])
        w = 8 * int(self.data[5])
        h = 8

        xy = (x, y, x + w, y + h)
        image.rectangle(xy, fill=255)

class String(Data):

    def __init__(self):
        super().__init__()

        self.data = ["typeString", 0, 0, 32, "stringLabel", 0, 0]
        self.name = ["t", "x", "y", "color", "pointer", "unused", "bg color"]

        self.other = StringData()

    def draw(self, image):
        x = int(self.data[1])
        y = int(self.data[2])
        w = 8 * len(self.other.data[0])
        h = 8

        xy = (x, y, x + w, y + h)
        image.rectangle(xy, fill=255*256)

class StringData(Data):

    def __init__(self):
        super().__init__()

        self.data = ["string text here!"]
        self.name = ["string text"]

class Sprite(Data):
    def __init__(self):
        super().__init__()

        self.data = ["typeSprite", 8, 0, 0, 0, "spriteLabel", 12, 12]
        self.name = ["t", "bpp", "x", "y", "color", "pointer", "width", "height"]

    def draw(self, image):
        x = int(self.data[2])
        y = int(self.data[3])
        w = 8 * int(self.data[6])
        h = int(self.data[7])

        xy = (x, y, x + w, y + h)
        image.rectangle(xy, fill=255*65536)

class Box(Data):

    def __init__(self):
        super().__init__()

        self.data = ["typeBox", 0, 0, 0, 90, 1, 60]
        self.name = ["t", "x", "y", "color", "width", "bg color", "height"]

    def draw(self, image):
        x = int(self.data[1])
        y = int(self.data[2])
        w = int(self.data[4])
        h = int(self.data[6])

        xy = (x, y, x + w, y + h)
        image.rectangle(xy, fill=65535)

class Map(Data):

    def __init__(self):
        super().__init__()

        self.data = ["typeMap", 0, 0, 12, "field", 10, 20]
        self.name = ["t", "x", "y", "tilesize", "mapinfoptr", "width", "height"]

        self.other = MapAdditional()

    def draw(self, image):
        x = int(self.data[1])
        y = int(self.data[2])
        w = int(self.data[3]) * int(self.data[5])
        h = int(self.data[3]) * int(self.data[6])

        xy = (x, y, x + w, y + h)
        image.rectangle(xy, fill=65535*256)

class MapAdditional(Data):
    def __init__(self):
        super().__init__()

        self.data = [0, "mapDataPtr"]
        self.name = ["null tile", "mapdataptr"]

class Hold(Data):

    def __init__(self):
        super().__init__()

        self.data = ["typeHold", 124, 180, 12, "bg_box_ptr", 0, 0]
        self.name = ["t", "x", "y", "tile size?", "bg object ptr", "unused?", "unused?"]

        self.other = Box()

    def draw(self, image):
        self.other.draw(image)

        x = int(self.data[1])
        y = int(self.data[2])
        w = int(self.data[3]) * 4
        h = int(self.data[3]) * 2

        xy = (x, y, x + w, y + h)
        image.rectangle(xy, fill=255+255*65536)

class Preview(Data):

    def __init__(self):
        super().__init__()

        self.data = ["typePreview", "bg_obj", 0, "previewcoords", 6, 0]

        self.size = [1, 3, 1, 3, 1, 1]
        self.name = ["t", "bg obj ptr", "unused", "coordinates ptr", "# pieces", "unused"]

        self.other = PreviewCoords()

    def draw(self, image):
        self.other.draw(image)

class PreviewCoords(Data):

    def __init__(self):
        super().__init__()

        self.data = [136, 12, 136, 36, 136, 60, 136, 84, 136, 112, 136, 136]

        self.size = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
        self.name = ["x", "y", "x", "y", "x", "y", "x", "y", "x", "y", "x", "y"]

        self.other = Box()
        self.other.data = ["typeBox", 128, 6, 0, 32, 0, 160]

    def draw(self, image):
        self.other.draw(image)

        for i in range(0, 12, 2):
            x = int(self.data[i])
            y = int(self.data[i + 1])
            w = 6
            h = 6

            xy = (x, y, x + w, y + h)
            image.rectangle(xy, fill=16777215)

def create_object(index):
    return [Number, String, Sprite, Box, Map, Preview, Hold][index]()


item_types = ["Number", "String", "Sprite", "Box", "Map", "Preview", "Hold"]