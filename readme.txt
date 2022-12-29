CETrisDT converter v0.3
There are two separate programs currently.
* cetrisdt_conv.py, a script to convert images to graphics data.
* gui.py, a GUI for creating (and eventually modifying) object layouts.

gui.py is currently unfinished, and may or may not be completed.

cetrisdt_edit.py - This program is intended to convert images into CETris formatted data.
In it's current state, the program can convert...
 *palettes, stored as images
 *images
 *tilesets
 *tilemaps

Some examples of conversions:
Converting palette info:
./cetrisdt_conv.py --palette images/sample_palette.png --data palLabel palette
palLabel:
.db $00, $00, $ef, $3d, $18, $63, $ff, $7f

Converting sprites:
./cetrisdt_conv.py --palette images/sample_palette.png 2 --sprite images/sample_tile.png --data sprLabel sprite
sprLabel:
.db $55, $55, $55, $6a, $6a, $54, $65, $59
.db $54, $65, $59, $50, $6a, $59, $50, $55
.db $55, $40, $55, $55, $00, $55, $54, $00
.db $55, $50, $00, $55, $40, $3c, $50, $00
.db $3c, $00, $00, $00

Converting tilesets:
./cetrisdt_conv.py --palette images/sample_palette.png 2 --tileset images/sample_tileset.png 16 --data sprLabel sprite --data tileLabel tileset
sprLabel:
.db sp2bpp
.db $00, $00, $00, $00, $00, $00, $00, $00
.db $00, $00, $00, $00, $00, $00, $00, $00
.db $00, $00, $00, $00, $00, $00, $00, $00
.db $00, $00, $00, $00, $00, $00, $00, $00
(...many lines...)
.db $3f, $ff, $ff, $fc, $3f, $ff, $ff, $fc
.db $3f, $ff, $ff, $fc, $3f, $ff, $ff, $fc
.db $3f, $ff, $ff, $fc, $3f, $ff, $ff, $fc
.db $3f, $ff, $ff, $fc, $00, $00, $00, $00

tileLabel:
.db $00, $00
.db $01, $00
.db $02, $00
.db $03, $00
.db $04, $00
.db $05, $00
.db $06, $00
.db $07, $00

Converting maps:
./cetrisdt_conv.py --palette images/sample_palette.png 2 --tileset images/sample_tileset.png 16 --map images/sample_map.png 16 --data mapLabel map
mapLabel:
.db $01, $00, $00, $01
.db $05, $06, $07, $03
.db $03, $07, $06, $05
.db $01, $00, $00, $01

You can also specify a palette or tile offset for both "tileset" and "map" data. This is useful if you are using multiple images to store separate palette or sprite data - you can set the offset to adjust for more sprites or colors.
Example:
./cetrisdt_conv.py --palette images/sample_palette.png 2 --tileset images/sample_tileset.png 16 --map images/sample_map.png 16 --data tileLbl tileset 0 32 --data mapLabel map 4
tileLbl:
.db $00, $20
.db $01, $20
.db $02, $20
.db $03, $20
.db $04, $20
.db $05, $20
.db $06, $20
.db $07, $20

mapLabel:
.db $05, $04, $04, $05
.db $09, $0a, $0b, $07
.db $07, $0b, $0a, $09
.db $05, $04, $04, $05



gui.py - This program is for creating object layouts.

Functions:
Add - Add an object. A dialog will appear where you can select the object type.
Edit - Modify selected object.
Delete - Delete selected object.
Save - Convert all objects to data, printed to the console.

The colorful boxes mark the type of object previewed.
Red - number
Green - string
Blue - sprite
Yellow - box
White - preview (piece coordinates, background box is yellow)
Cyan - map (tilemap, also used for main field)
Pink - hold (range of held piece; background box is yellow.)

The output from this program needs to be copied and modified to function properly.
Trying to use the output directly will like cause compilation errors,
or if not, potentially crash upon loading.

Use the default tetrice_dat.asm as a template if trying to create your own data file.
