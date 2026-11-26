# News of Wednesday 25 November 2026, drawn as one front-page image.
# Pure standard library: the picture is painted pixel by pixel and written
# as a PNG, so the grader needs nothing installed and every run is identical.

import os
import struct
import zlib

W = 1024
H = 1024

INK = (20, 33, 61)
PAPER = (247, 243, 234)
WHITE = (255, 255, 255)
RED = (190, 45, 45)
ORANGE = (230, 126, 34)
YELLOW = (250, 200, 60)
TEAL = (14, 116, 144)
GREEN = (34, 120, 70)
GOLD = (201, 145, 20)
SKY = (160, 205, 238)
SEA = (23, 84, 140)
DARK = (25, 28, 38)
GRAY = (105, 110, 120)
SMOKE = (150, 152, 158)
SAND = (232, 213, 165)

FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11100", "10010", "10001", "10001", "10001", "10010", "11100"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "10101", "01010"),
    "X": ("10001", "01010", "00100", "00100", "00100", "01010", "10001"),
    "Y": ("10001", "01010", "00100", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11111", "00010", "00100", "00010", "00001", "10001", "01110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("00110", "01000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00010", "01100"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    "-": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "+": ("00000", "00100", "00100", "01110", "00100", "00100", "00000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
}


class Canvas:
    def __init__(self, width, height, color):
        self.w = width
        self.h = height
        self.px = bytearray(bytes(color) * width * height)

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(color)

    def rect(self, x0, y0, x1, y1, color):
        for y in range(max(0, y0), min(self.h, y1)):
            base = y * self.w * 3
            row = bytes(color) * (min(self.w, x1) - max(0, x0))
            start = base + max(0, x0) * 3
            self.px[start:start + len(row)] = row

    def frame(self, x0, y0, x1, y1, color, thick=3):
        self.rect(x0, y0, x1, y0 + thick, color)
        self.rect(x0, y1 - thick, x1, y1, color)
        self.rect(x0, y0, x0 + thick, y1, color)
        self.rect(x1 - thick, y0, x1, y1, color)

    def circle(self, cx, cy, r, color):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
                    self.set(x, y, color)

    def ring(self, cx, cy, r, color, thick=3):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d = (x - cx) * (x - cx) + (y - cy) * (y - cy)
                if (r - thick) * (r - thick) <= d <= r * r:
                    self.set(x, y, color)

    def line(self, x0, y0, x1, y1, color, thick=3):
        steps = max(abs(x1 - x0), abs(y1 - y0), 1)
        for s in range(steps + 1):
            x = x0 + (x1 - x0) * s // steps
            y = y0 + (y1 - y0) * s // steps
            self.rect(x - thick // 2, y - thick // 2,
                      x - thick // 2 + thick, y - thick // 2 + thick, color)

    def tri(self, ax, ay, bx, by, cx, cy, color):
        top = min(ay, by, cy)
        bot = max(ay, by, cy)
        for y in range(top, bot + 1):
            xs = []
            for (px, py, qx, qy) in ((ax, ay, bx, by), (bx, by, cx, cy), (cx, cy, ax, ay)):
                if py == qy:
                    continue
                if min(py, qy) <= y <= max(py, qy):
                    xs.append(px + (qx - px) * (y - py) // (qy - py))
            if len(xs) >= 2:
                self.rect(min(xs), y, max(xs) + 1, y + 1, color)

    def text_w(self, text, scale):
        return len(text) * (5 * scale + scale) - scale

    def text(self, x, y, text, scale, color):
        cx = x
        for ch in text.upper():
            glyph = FONT.get(ch, FONT[" "])
            for row_i, row in enumerate(glyph):
                for col_i, bit in enumerate(row):
                    if bit == "1":
                        self.rect(cx + col_i * scale, y + row_i * scale,
                                  cx + col_i * scale + scale, y + row_i * scale + scale, color)
            cx += 5 * scale + scale
        return cx

    def centered(self, cx, y, text, scale, color):
        self.text(cx - self.text_w(text, scale) // 2, y, text, scale, color)


def png_bytes(canvas):
    raw = bytearray()
    stride = canvas.w * 3
    for y in range(canvas.h):
        raw.append(0)
        raw += canvas.px[y * stride:(y + 1) * stride]

    def chunk(tag, data):
        body = tag + data
        return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", canvas.w, canvas.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b""))


def flame(c, x, y, s):
    c.tri(x, y - 3 * s, x - s, y, x + s, y, RED)
    c.tri(x, y - 2 * s, x - s // 2, y, x + s // 2, y, ORANGE)
    c.tri(x, y - s, x - s // 3, y, x + s // 3, y, YELLOW)


def tanker(c, x, y, flip):
    hull = RED if flip else DARK
    c.rect(x, y, x + 230, y + 30, hull)
    c.tri(x, y, x - 28, y + 30, x, y + 30, hull)
    c.tri(x + 230, y, x + 258, y + 30, x + 230, y + 30, hull)
    c.rect(x + 26, y - 20, x + 72, y, WHITE)
    c.rect(x + 32, y - 14, x + 66, y - 7, INK)
    c.rect(x + 104, y - 12, x + 164, y, GRAY)
    c.rect(x + 166, y - 36, x + 180, y, DARK)
    flame(c, x + 122, y - 10, 22)
    flame(c, x + 152, y - 8, 17)
    c.circle(x + 134, y - 72, 17, SMOKE)
    c.circle(x + 162, y - 90, 12, SMOKE)
    c.circle(x + 112, y - 88, 10, SMOKE)


def mine(c, x, y):
    c.circle(x, y, 13, DARK)
    for dx, dy in ((0, -20), (0, 20), (-20, 0), (20, 0), (-14, -14), (14, -14), (-14, 14), (14, 14)):
        c.line(x, y, x + dx, y + dy, DARK, 4)
    c.circle(x - 4, y - 4, 3, GRAY)


def hero(c):
    x0, y0, x1, y1 = 24, 166, 1000, 462
    c.rect(x0, y0, x1, y0 + 104, SKY)
    c.rect(x0, y0 + 104, x1, y0 + 140, (110, 170, 220))
    c.rect(x0, y0 + 140, x1, y1 - 84, SEA)
    for i in range(14):
        wx = x0 + 30 + i * 68
        c.line(wx, y0 + 186 + (i % 3) * 7, wx + 34, y0 + 186 + (i % 3) * 7, (90, 150, 205), 3)
    c.circle(x0 + 880, y0 + 44, 26, YELLOW)
    tanker(c, x0 + 80, y0 + 148, False)
    tanker(c, x0 + 570, y0 + 156, True)
    mine(c, x0 + 410, y0 + 182)
    mine(c, x0 + 478, y0 + 196)
    c.frame(x0, y0, x1, y1, INK, 4)
    c.rect(x0, y1 - 84, x1, y1, INK)
    c.centered(512, y1 - 78, "HORMUZ: 2 TANKERS BURN", 6, WHITE)
    c.centered(512, y1 - 32, "IRAN SAYS MINES HIT SHIPS + HOUTHIS CLAIM SAUDI REFINERY FIRE", 2, YELLOW)


def panel(c, x0, y0, tag, tag_color, head_lines, sub_lines, icon):
    x1, y1 = x0 + 480, y0 + 152
    c.rect(x0, y0, x1, y1, WHITE)
    c.frame(x0, y0, x1, y1, INK, 3)
    c.rect(x0, y0, x0 + 170, y0 + 26, tag_color)
    c.text(x0 + 10, y0 + 6, tag, 2, WHITE)
    icon(c, x1 - 86, y0 + 62)
    y = y0 + 38
    for line in head_lines:
        c.text(x0 + 14, y, line, 4, INK)
        y += 34
    y += 2
    for line in sub_lines:
        c.text(x0 + 14, y, line, 2, GRAY)
        y += 19


def icon_building(c, x, y):
    c.rect(x - 34, y - 22, x - 8, y + 36, GRAY)
    c.rect(x + 2, y - 34, x + 30, y + 36, INK)
    for wy in range(y - 14, y + 28, 12):
        c.rect(x - 28, wy, x - 14, wy + 6, YELLOW)
        c.rect(x + 8, wy - 6, x + 22, wy, YELLOW)
    flame(c, x + 16, y - 30, 12)


def icon_rocket(c, x, y):
    c.circle(x + 26, y - 34, 5, GOLD)
    c.circle(x - 30, y - 20, 4, GOLD)
    c.circle(x - 22, y + 30, 4, GOLD)
    c.tri(x, y - 48, x - 14, y - 20, x + 14, y - 20, RED)
    c.rect(x - 14, y - 20, x + 14, y + 22, WHITE)
    c.frame(x - 14, y - 20, x + 14, y + 22, INK, 2)
    c.circle(x, y - 2, 6, TEAL)
    c.tri(x - 14, y + 8, x - 28, y + 26, x - 14, y + 22, RED)
    c.tri(x + 14, y + 8, x + 28, y + 26, x + 14, y + 22, RED)
    flame(c, x, y + 42, 14)


def icon_island(c, x, y):
    c.rect(x - 42, y + 18, x + 42, y + 26, SEA)
    c.tri(x - 36, y + 18, x, y - 6, x + 36, y + 18, GREEN)
    c.line(x, y - 6, x, y - 42, DARK, 3)
    c.tri(x, y - 42, x + 26, y - 34, x, y - 26, RED)
    c.circle(x - 28, y - 26, 8, YELLOW)


def icon_drone(c, x, y):
    c.line(x - 26, y - 18, x + 26, y + 18, DARK, 4)
    c.line(x - 26, y + 18, x + 26, y - 18, DARK, 4)
    c.circle(x, y, 8, RED)
    for dx, dy in ((-26, -18), (26, -18), (-26, 18), (26, 18)):
        c.ring(x + dx, y + dy, 9, GRAY, 3)
    c.rect(x - 30, y + 30, x - 8, y + 44, SAND)
    c.rect(x + 6, y + 30, x + 30, y + 44, SAND)


def icon_globe(c, x, y):
    c.circle(x, y, 34, TEAL)
    c.circle(x - 12, y - 10, 10, GREEN)
    c.circle(x + 14, y + 8, 12, GREEN)
    c.circle(x + 4, y - 20, 7, GREEN)
    c.line(x - 6, y - 30, x + 2, y - 8, RED, 3)
    c.line(x + 2, y - 8, x - 4, y + 14, RED, 3)
    c.line(x - 4, y + 14, x + 6, y + 30, RED, 3)
    c.circle(x + 34, y - 34, 10, YELLOW)


def icon_chip(c, x, y):
    c.rect(x - 26, y - 26, x + 26, y + 26, DARK)
    c.rect(x - 14, y - 14, x + 14, y + 14, GOLD)
    for off in (-18, -6, 6, 18):
        c.line(x + off, y - 26, x + off, y - 38, GRAY, 4)
        c.line(x + off, y + 26, x + off, y + 38, GRAY, 4)
        c.line(x - 26, y + off, x - 38, y + off, GRAY, 4)
        c.line(x + 26, y + off, x + 38, y + off, GRAY, 4)
    c.line(x - 20, y + 20, x + 20, y - 20, RED, 5)


def draw():
    c = Canvas(W, H, PAPER)
    c.rect(0, 0, W, 150, INK)
    c.centered(512, 18, "WORLD NEWS", 11, WHITE)
    c.centered(512, 104, "WEDNESDAY 25 NOVEMBER 2026", 4, YELLOW)
    c.rect(0, 150, W, 158, RED)
    hero(c)
    panel(c, 24, 474, "EUROPE", RED,
          ("ODESA + KYIV", "HIT"),
          ("RUSSIAN STRIKES KILL 2 IN ODESA,", "SET A KYIV APARTMENT BLOCK ABLAZE"), icon_building)
    panel(c, 520, 474, "SPACE", TEAL,
          ("PAKISTAN", "REACHES ORBIT"),
          ("SHENZHOU-24 CARRIES FIRST FOREIGN", "ASTRONAUT TO CHINA'S TIANGONG"), icon_rocket)
    panel(c, 24, 634, "PACIFIC", GREEN,
          ("NO FOREIGN", "BASE"),
          ("AUSTRALIA + SOLOMON ISLANDS", "SIGN TREATY BARRING FOREIGN BASES"), icon_island)
    panel(c, 520, 634, "AFRICA", ORANGE,
          ("SUDAN DRONES", "KILL 19"),
          ("RSF STRIKES HIT HOMES IN", "DAMAZIN + ROSEIRES, SAY LAWYERS"), icon_drone)
    panel(c, 24, 794, "CLIMATE", TEAL,
          ("COP31:", "NO DEAL"),
          ("POPE LEO XIV WARNS EXTREME", "CLIMATE EVENTS ARE RISING"), icon_globe)
    panel(c, 520, 794, "TECH", GOLD,
          ("HUAWEI GUILTY", "IN US COURT"),
          ("JURY CONVICTS ON TRADE SECRETS", "+ BANK FRAUD, 10 OF 12 COUNTS"), icon_chip)
    c.rect(24, 954, 1000, 1006, INK)
    c.centered(512, 962, "ALSO: GAZA STRIKE KILLS HAMAS SECURITY CHIEF", 2, WHITE)
    c.centered(512, 984, "US READIES NEW TARIFFS ON CHINA, EU + 14 ECONOMIES", 2, YELLOW)
    return c


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw())
    with open(os.path.join(out_dir, "entry.png"), "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
