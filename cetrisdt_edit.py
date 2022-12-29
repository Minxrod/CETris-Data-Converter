import converter

pal = []
tiles = []
data = []
tilemap = []


def edit_help(args):
	if len(args) > 1:
		help_cmd = args[1]

		for command in commands:
			if help_cmd == command[0]:
				print(command[0] + " " + command[1])
	else:
		print("List of commands: ")
		for command in commands:
			print(command[0] + " " + command[1])


def palette(args):
	global pal

	b = 8
	if len(args) > 2:
		b = int(args[2])

	pal = converter.convert_file_to_palette(args[1], b=b)  # generate.convert_file_to_palette(args[1])


def tile(args):
	global data

	# if pal is None:
	#	 palette(args)

	data = [converter.convert_file_simple(args[1], pal)]  # generate.convert_file_to_data(args[1], pal)


def tileset(args):
	global tiles, data

	tiles = []
	data = []

	img_dat = converter.load_file(args[1])
	pix = img_dat[0]
	w = img_dat[1]
	h = img_dat[2]

	if len(args) > 2:
		size = int(args[2])
	else:
		size = 16

	b = len(pal[0])
	for y in range(0, h, size):
		for x in range(0, w, size):
			tile_data = converter.convert_image_to_data(pix, x, y, size, size, pal, adjust=False)
			tile_adjusted = converter.adjust_data(tile_data, b)
			tile_palette = min(tile_data) // b * b

			if tile_adjusted not in data:  # help prevent palette swaps from hogging memory
				data.append(tile_adjusted)
			tiles.append((data.index(tile_adjusted), tile_palette))


def load_map(args):
	global tilemap

	tilemap = []

	img_dat = converter.load_file(args[1])
	pix = img_dat[0]
	w = img_dat[1]
	h = img_dat[2]

	if len(args) > 2:
		size = int(args[2])
	else:
		size = 16

	b = len(pal[0])
	for y in range(0, h, size):
		tilemap.append([])
		for x in range(0, w, size):
			tile_data = converter.convert_image_to_data(pix, x, y, size, size, pal, adjust=False)
			tile_adjusted = converter.adjust_data(tile_data, b)
			tile_palette = min(tile_data) // b * b

			tile_info = (data.index(tile_adjusted), tile_palette)
			tilemap[-1].append(tiles.index(tile_info))


def output(args):
	offset = offset2 = 0
	if len(args) > 2:
		offset = int(args[2])
	if len(args) > 3:
		offset2 = int(args[3])

	convdat = None
	if args[1] == "palette":
		if pal is not None:
			conv_pal = []
			for subpal in pal:
				conv_pal.append([])
				for item in subpal:
					val = (int(item[0] / 8) << 10) + (int(item[1] / 8) << 5) + (int(item[2] / 8))
					conv_pal[-1].append(val % 256)
					conv_pal[-1].append(val // 256)

			convdat = converter.convert_lists_to_db(conv_pal, 8)
	elif args[1] == "tile":
		if data is not None:
			convdat = converter.convert_lists_to_db(data, converter.col[len(pal[0])], per_line=offset if offset else None)
	elif args[1] == "tileset":
		if tiles is not None:
			convdat = converter.convert_lists_to_db([[x[0] + offset, x[1] + offset2] for x in tiles], 8)
	elif args[1] == "map":
		if tilemap is not None:
			convdat = converter.convert_lists_to_db([[y + offset for y in x] for x in tilemap], 8)
	else:
		print("Error: Invalid data type\nPlease choose from: palette, tile, tileset, map")
		return

	print(args[1] + ":\n" + convdat)


commands = [["help", "[command]", 0, 1, edit_help],
			["exit", "", 0, 0, exit],
			["palette", "filename [bpp]", 1, 2, palette],
			["tile", "filename", 1, 1, tile],
			["map", "filename [tile_size]", 1, 2, load_map],
			["tileset", "filename [tile_size]", 1, 2, tileset],
			["print", "datatype [offset] [offset2]", 1, 3, output]]

select = ""
arg = []

while select != "exit":
	try:
		select = input("? ")
		
		arg = select.split()
		arg_len = len(arg) - 1
		cmd_len = len(select)
		
		for cmd in commands:
			if cmd[0] == arg[0]:
				if cmd[2] <= arg_len <= cmd[3]:
					cmd[4](arg)
				else:
					print("Wrong number of arguments")
	except Exception as e:
		print(e)

