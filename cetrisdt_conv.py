#!/usr/bin/env python3
import argparse
import sys

import converter

pal = []
tiles = []
data = []
tilemap = []

def palette(args):
	"""
	filename bpp
	"""
	global pal

	b = int(args[1])

	pal = converter.convert_file_to_palette(args[0], b=b)  # generate.convert_file_to_palette(args[1])


def tile(args):
	global data

	# if pal is None:
	#	 palette(args)

	data = [converter.convert_file_simple(args[0], pal)]  # generate.convert_file_to_data(args[1], pal)


def tileset(args):
	global tiles, data

	tiles = []
	data = []

	img_dat = converter.load_file(args[0])
	pix = img_dat[0]
	w = img_dat[1]
	h = img_dat[2]

	size = int(args[1])

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

	img_dat = converter.load_file(args[0])
	pix = img_dat[0]
	w = img_dat[1]
	h = img_dat[2]

	size = int(args[1])

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
	"""
	label type [offset] [offset2]
	"""
	offset = offset2 = 0
	if len(args) > 2:
		offset = int(args[2])
	if len(args) > 3:
		offset2 = int(args[3])

	convdat = None
	if args[1] == "palette":
		if pal:
			conv_pal = []
			for subpal in pal:
				conv_pal.append([])
				for item in subpal:
					val = (int(item[0] / 8) << 10) + (int(item[1] / 8) << 5) + (int(item[2] / 8))
					conv_pal[-1].append(val % 256)
					conv_pal[-1].append(val // 256)

			convdat = converter.convert_lists_to_db(conv_pal, 8)
	elif args[1] == "sprite":
		if data:
			convdat = f".db sp{converter.col[len(pal[0])]}bpp\n" if tiles else ""
			convdat += converter.convert_lists_to_db(data, converter.col[len(pal[0])], per_line=offset if offset else None)
		else:
			print(f"Error: Sprite data does not exist")
			return
	elif args[1] == "tileset":
		if tiles:
			convdat = converter.convert_lists_to_db([[x[0] + offset, x[1] + offset2] for x in tiles], 8)
		else:
			print(f"Error: Tileset data does not exist")
			return
	elif args[1] == "map":
		if tilemap:
			convdat = converter.convert_lists_to_db([[y + offset for y in x] for x in tilemap], 8)
		else:
			print(f"Error: Map data does not exist")
			return
	else:
		print(f"Error: Invalid data type '{args[1]}'\nPlease choose from: palette, sprite, tileset, map")
		return

	print(args[0] + ":\n" + convdat)


parser = argparse.ArgumentParser(prog="CEtris image converter", description="CEtrisDT conversion tools.")

parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.3 (c) 2020-2022")

parser.add_argument("-p", "--palette", dest="palette", nargs=2, metavar=("filename","bpp"), help="source palette image")
parser.add_argument("-s", "--sprite", dest="sprite", nargs=1, metavar="filename", help="source sprite image")
parser.add_argument("-t", "--tileset", dest="tileset", nargs=2, metavar=("filename", "tile_size"), help="source tileset image")
parser.add_argument("-m", "--map", dest="map", nargs=2, metavar=("filename", "tile_size"), help="source map image")

parser.add_argument("-d", "--data", dest="format", action="append", default=[], nargs='*', help="Specify output format. Provide a label name and type, and optionally a data offset.")

args = parser.parse_args()

print(args)

if not args.format:
	print("No output specified!")
	sys.exit(1)

if args.palette:
	if int(args.palette[1]) not in [1,2,4,8]:
		print("Invalid BPP specified")
		sys.exit(1)
	palette(args.palette)
if args.sprite:
	if not pal:
		print("Palette file not specified")
		sys.exit(1)
	tile(args.sprite)
if args.tileset:
	if not pal:
		print("Palette file not specified")
		sys.exit(1)
	tileset(args.tileset)
if args.map:
	if not pal:
		print("Palette file not specified")
		sys.exit(1)
	if not tiles:
		print("Tileset not specified")
		sys.exit(1)
	load_map(args.map)

if args.format:
	for form in args.format:
		if not 2 <= len(form) <= 4:
			print("Invalid number of arguments")
			sys.exit(1)
		output(form)
