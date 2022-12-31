from typing import Dict, Tuple

import neopixel_spi as neopixel

NUM_PIXELS = 12
PIXEL_ORDER = neopixel.GRB

# Pre-defined colors
COLOR_PURPLE = 0x6A0DAD
COLOR_AQUA = 0x00FFFF
COLOR_ORANGE = 0xF5A506
COLOR_YELLOW = 0xC1E300
COLOR_NOT_QUITE_BLUE = 0x001EE3
COLOR_BLACK = 0x000000

COLOR_RED = 0xFF0000
COLOR_GREEN = 0x00FF00
COLOR_BLUE = 0x0000FF

# RGB
RGB_COLORS = (COLOR_RED, COLOR_GREEN, COLOR_BLUE)

# LED positions
VIO_LED = 1
PCC_LED = 2
THERMAL_LED = 3
FCC_LED = 4
APRIL_LED = 5

# delay in seconds
DELAY = 0.1

# lookup of topic prefixes to led position and color
STATUS_LOOKUP: Dict[str, Tuple[int, int]] = {
    "avr/vio": (VIO_LED, COLOR_PURPLE),
    "avr/pcm": (PCC_LED, COLOR_AQUA),
    "avr/fcm": (FCC_LED, COLOR_ORANGE),
    "avr/thermal": (THERMAL_LED, COLOR_NOT_QUITE_BLUE),
    "avr/apriltags": (APRIL_LED, COLOR_YELLOW),
}
