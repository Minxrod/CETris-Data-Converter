CETrisDT converter v0.2
There are two separate programs currently.
* cetrisdt_edit.py, a script to convert images to graphics data.
* gui.py, a GUI for creating (and eventually modifying) object layouts.

Both programs are unfinished and will eventually be combined. For now, these
can be used to convert data for manual editing and copying to tetrice_dat.asm

cetrisdt_edit.py - This program is intended to convert images into CETris formatted data.
In it's current state, the program can convert...
 *palettes, stored as images
 *images
 *tilesets
 *tilemaps

Some examples of conversions:
Converting palette info:
? palette images/sample_palette.png
? print palette
palette:
.db $00, ...

Converting sprites:
? palette images/sample_palette.png
? tile images/sample_tile.png
? print tile
tile:
.db $55, ...

Converting tilesets:
? palette images/sample_palette.png
? tileset images/sample_tileset.png
? print tileset
tileset:
.db $00, $00
...
? print tile
tile:
.db $00, ...
...

Converting maps:
? palette images/sample_palette.png
? tileset images/sample_tileset.png
? map images/sample_map.png
? print palette
...
? print tileset
...
? print map
.db $01, ...

Notes: When converting a tileset, the tile/palette pairs are output by tileset.
The actual sprite data is output by tile, with all tiles converted one after the other.
You can also specify a palette or tile offset for both "tileset" and "map" data.

? palette images/sample_palette.png
? tileset images/sample_tileset.png
? print tileset 8 64
.db $08, $64 ;as opposed to $00, $00
...
? map images/sample_map.png
? print map 8
.db $09, ... ;instead of $01, ...

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