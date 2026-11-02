#!/usr/bin/env python3
"""Render one GBA screen to a PNG from a raw memory dump.

  python3 render_gba.py dump_N.bin out.png

The dump (written by gdb_dump.py) is these GBA memory regions back to back:
    0x60    bytes of I/O registers   (display control, background settings, scroll)
    0x400   bytes of palette RAM     (512 colours: 256 for backgrounds, 256 for sprites)
    0x18000 bytes of VRAM            (tile graphics + tilemaps, sprite graphics at +0x10000)
    0x400   bytes of OAM             (128 sprite entries)

It redraws the frame the way the GBA would in "mode 0" (four tiled background
layers plus sprites). It's a simple software renderer: it ignores colour
blending, windows (masking) and sprite rotation/scaling. Pokemon menus barely use
those, so the result is close enough to check the UI. A stray magenta border or a
slightly offset cursor are renderer artefacts, not bugs in the game.
"""
import sys, struct, zlib

d = open(sys.argv[1], 'rb').read()
# Split the dump back into the four memory regions (see layout above)
io, pal, vram, oam = d[:0x60], d[0x60:0x460], d[0x460:0x18460], d[0x18460:0x18860]


def r16(buf, offset):
    """Read a little-endian 16-bit value."""
    return struct.unpack_from('<H', buf, offset)[0]


def color(i):
    """Palette entry i -> (r, g, b). GBA colours are 15-bit BGR555, so scale 5-bit channels to 8-bit."""
    c = r16(pal, i * 2)
    return ((c & 31) << 3, (c >> 5 & 31) << 3, (c >> 10 & 31) << 3)


dispcnt = r16(io, 0)  # DISPCNT: which layers are switched on, sprite tile mapping mode
W, H = 240, 160       # GBA screen size

# Start with every pixel set to the backdrop colour (palette entry 0)
img = [[color(0)] * W for _ in range(H)]

# --- Work out the drawing order -------------------------------------------
# Every background and sprite has a priority 0-3 (0 = in front). Within one
# priority, sprites go in front of backgrounds, lower-numbered backgrounds go in
# front of higher-numbered ones, and lower-numbered sprites go in front of
# higher-numbered ones. Build a list of (priority, tie-break, kind, params) and
# sort it back-to-front so we can just paint over in order.
layers = []
for bg in range(4):
    if not dispcnt & (0x100 << bg):          # DISPCNT bits 8-11 enable BG0-BG3
        continue
    cnt = r16(io, 8 + bg * 2)                # BGxCNT: priority, tile/map base, colour depth, size
    hofs = r16(io, 0x10 + bg * 4) & 511      # BGxHOFS: horizontal scroll
    vofs = r16(io, 0x12 + bg * 4) & 511      # BGxVOFS: vertical scroll
    layers.append((cnt & 3, -10 + bg, 'bg', (cnt, hofs, vofs)))
if dispcnt & 0x1000:                         # DISPCNT bit 12 enables sprites
    for n in range(127, -1, -1):
        a0, a1, a2 = struct.unpack_from('<HHH', oam, n * 8)  # each OAM entry is 3 attributes + 1 unused
        if (a0 >> 8 & 3) == 2:               # attr0 bits 8-9 == 2 means "sprite disabled"
            continue
        layers.append((a2 >> 10 & 3, -20 - n, 'obj', (a0, a1, a2)))
layers.sort(key=lambda l: (-l[0], -l[1]))    # back-most first

# Sprite pixel size, looked up by (shape, size) from attr0 bits 14-15 and attr1 bits 14-15
SPRITE_SIZES = {
    (0, 0): (8, 8),   (0, 1): (16, 16), (0, 2): (32, 32), (0, 3): (64, 64),   # square
    (1, 0): (16, 8),  (1, 1): (32, 8),  (1, 2): (32, 16), (1, 3): (64, 32),   # wide
    (2, 0): (8, 16),  (2, 1): (8, 32),  (2, 2): (16, 32), (2, 3): (32, 64),   # tall
}

for _, _, kind, p in layers:
    if kind == 'bg':
        # --- Tiled background layer --------------------------------------
        cnt, hofs, vofs = p
        char_base = (cnt >> 2 & 3) * 0x4000   # where this layer's 8x8 tile graphics start in VRAM
        screen_base = (cnt >> 8 & 31) * 0x800  # where its tilemap (which tile goes where) starts
        bpp8 = cnt >> 7 & 1                   # 0 = 16-colour tiles (4bpp), 1 = 256-colour tiles (8bpp)
        size = cnt >> 14                      # map size: 256 or 512 pixels in each direction
        map_w = 512 if size & 1 else 256
        map_h = 512 if size & 2 else 256
        for y in range(H):
            for x in range(W):
                # Screen pixel -> position on the (scrolled, wrapping) background map
                X, Y = (x + hofs) % map_w, (y + vofs) % map_h
                # Big maps are made of 256x256 blocks, each its own 32x32 tilemap
                block = (X // 256) + (Y // 256) * (2 if map_w == 512 else 1)
                # Tilemap entry: bits 0-9 tile number, 10 h-flip, 11 v-flip, 12-15 palette
                entry = r16(vram, screen_base + block * 0x800 + ((Y % 256) // 8 * 32 + (X % 256) // 8) * 2)
                tx, ty = X % 8, Y % 8                 # pixel position inside the 8x8 tile
                if entry & 0x400:
                    tx = 7 - tx
                if entry & 0x800:
                    ty = 7 - ty
                tile = entry & 0x3ff
                if bpp8:
                    # 8bpp: one byte per pixel, 64 bytes per tile, index into the full 256-colour palette
                    o = char_base + tile * 64 + ty * 8 + tx
                    if o >= 0x10000:  # background tiles can't reach into sprite VRAM
                        continue
                    v = vram[o]
                    ci = v
                else:
                    # 4bpp: two pixels per byte (low nibble first), 32 bytes per tile,
                    # index into one of 16 sub-palettes chosen by the tilemap entry
                    o = char_base + tile * 32 + ty * 4 + tx // 2
                    if o >= 0x10000:
                        continue
                    v = (vram[o] >> (4 * (tx & 1))) & 15
                    ci = (entry >> 12) * 16 + v
                if v:  # colour 0 is transparent
                    img[y][x] = color(ci)
    else:
        # --- Sprite (OBJ) -------------------------------------------------
        a0, a1, a2 = p
        w, h = SPRITE_SIZES.get((a0 >> 14, a1 >> 14), (8, 8))
        oy, ox = a0 & 255, a1 & 511          # top-left position; values wrap, so convert to signed
        if ox >= 256:
            ox -= 512
        if oy >= 160:
            oy -= 256
        affine = a0 >> 8 & 1                 # rotation/scaling sprite (drawn unrotated here)
        if affine and a0 >> 9 & 1:           # "double size" affine sprites are offset by half their size
            ox += w // 2
            oy += h // 2
        bpp8 = a0 >> 13 & 1
        tile = a2 & 0x3ff                    # first tile of the sprite graphics
        palno = a2 >> 12                     # 16-colour sub-palette (4bpp only)
        hflip = (not affine) and a1 >> 12 & 1
        vflip = (not affine) and a1 >> 13 & 1
        one_d = dispcnt >> 6 & 1             # 1D mapping: a sprite's tiles are consecutive in VRAM;
                                             # 2D mapping: VRAM is a 32-tile-wide grid
        for yy in range(h):
            for xx in range(w):
                sx, sy = ox + xx, oy + yy
                if not (0 <= sx < W and 0 <= sy < H):
                    continue
                tx = w - 1 - xx if hflip else xx
                ty = h - 1 - yy if vflip else yy
                # Sprite graphics live at VRAM + 0x10000 and use palette entries 256-511
                if bpp8:
                    # 8bpp tiles take two 32-byte tile slots each
                    tn = tile + ((ty // 8) * (w // 8) * 2 if one_d else (ty // 8) * 32) + (tx // 8) * 2
                    v = vram[0x10000 + (tn & 0x3ff) * 32 + (ty % 8) * 8 + tx % 8]
                    ci = 256 + v
                else:
                    tn = tile + ((ty // 8) * (w // 8) if one_d else (ty // 8) * 32) + tx // 8
                    b = vram[0x10000 + (tn & 0x3ff) * 32 + (ty % 8) * 4 + (tx % 8) // 2]
                    v = (b >> (4 * (tx & 1))) & 15
                    ci = 256 + palno * 16 + v
                if v:  # colour 0 is transparent
                    img[sy][sx] = color(ci)

# --- Write the PNG (scaled up 3x so it's easy to see) ---------------------
SCALE = 3
# PNG image data: each row starts with a filter-type byte (0 = none), then RGB triples
raw = b''.join(
    b'\x00' + b''.join(bytes(img[y // SCALE][x // SCALE]) for x in range(W * SCALE))
    for y in range(H * SCALE))


def chunk(tag, data):
    """One PNG chunk: length, 4-letter tag, data, CRC32 of tag+data."""
    return struct.pack('>I', len(data)) + tag + data + struct.pack('>I', zlib.crc32(tag + data) & 0xffffffff)


# IHDR = width, height, 8 bits per channel, colour type 2 (RGB), no interlace
open(sys.argv[2], 'wb').write(
    b'\x89PNG\r\n\x1a\n'
    + chunk(b'IHDR', struct.pack('>IIBBBBB', W * SCALE, H * SCALE, 8, 2, 0, 0, 0))
    + chunk(b'IDAT', zlib.compress(raw))
    + chunk(b'IEND', b''))
