CETrisDT converter v0.1

This program is intended to convert images into CETris formatted data. 
In it's current state, the program can convert...
 *palettes, stored as images
 *images
 *tilesets
 *tilemaps

The eventual goal of this program is to make creating custom themes for CETris much easier than it currently is.
For now, all it does is convert graphics data, requiring the information to be manually copied to the .asm file.

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
To convert a tileset or map that doesn't include tetris block sprites or palette info, you can add an offset like this:

? palette images/sample_palette.png
? tileset images/sample_tileset.png
? print tileset 8 64
.db $08, $64 ;as opposed to $00, $00
...
? map images/sample_map.png
? print map 8
.db $09, ... ;instead of $01, ...