# NeoPixel Matrix for MicroPython

The `NeoPixelMatrix` module is a simple library to display text and graphics on a NeoPixel LED matrix using MicroPython. This module provides an easy way to control the LED matrix, including scrolling text, setting colors, and adjusting the brightness. This library was specifically written for an 8x32 WS2812b Matrix and has been tested on ESP32.

## Features

- 🔤 Display text in multiple colors
- ↔️ Scroll text horizontally
- 🌈 Fill the entire matrix with a specified color
- 🧹 Clear the matrix with a single command
- 💡 Control the brightness of the display
- 🔄 Support for both horizontal and vertical LED matrices
- 🎨 Predefined color constants and helper functions

## Installation

To use the `NeoPixelMatrix` module, simply copy the `neopixel_matrix.py` file to your MicroPython board.

## Usage

Here is an example of how to use the `NeoPixelMatrix` module:

```python
from neopixel_matrix import NeoPixelMatrix, Color

# create a NeoPixelMatrix instance
matrix = NeoPixelMatrix(pin=5, width=16, height=8)

# set the brightness of the matrix
matrix.brightness = 0.5

# fill the entire matrix with a color
matrix.fill(Color.RED)
matrix.show()

# display text on the matrix
matrix.text("Hello", 0, 0, Color.GREEN)
matrix.show()

# scroll the text horizontally
matrix.scroll(delay=0.1)
```

## API Reference

### NeoPixelMatrix

#### `__init__(self, pin, width, height, direction=HORIZONTAL, brightness=1.0)`

Create a new `NeoPixelMatrix` instance.

- `pin`: The pin number where the NeoPixel data line is connected.
- `width`: The width of the NeoPixel matrix in pixels.
- `height`: The height of the NeoPixel matrix in pixels.
- `direction`: The direction of the NeoPixel matrix (either `HORIZONTAL` or `VERTICAL`).
- `brightness`: The initial brightness of the display (a value between 0 and 1).

#### `fill(self, color)`

Fill the entire matrix with the specified color.

- `color`: The color to fill the matrix with, as an (R, G, B) tuple.

#### `show(self)`

Update the display to show the current framebuffer contents.

#### `clear(self)`

Clear the matrix by setting all pixels to black and update the display.

#### `text(self, string, x, y, color)`

Display a string of text on the matrix at the specified position and color.

- `string`: The text to display.
- `x`: The horizontal position of the text.
- `y`: The vertical position of the text.
- `color`: The color of the text, as an (R, G, B) tuple.

#### `scroll(self, delay=0.1, scroll_out=True)`

Scroll the text horizontally with the specified delay between frames.

- `delay`: The time (in seconds) to wait between each frame.
- `scroll_out`: If `True`, scroll the text out of the matrix; if `False`, stop scrolling once the last character is fully visible.

### Color

The `Color` class provides constants and helper functions for working with colors.

#### Constants

- `RED`
- `GREEN`
- `BLUE`
- `WHITE`
- `YELLOW`
- `CYAN`
- `MAGENTA`
- `BLACK`

#### `random()`

Return a random color as an (R, G, B) tuple.

#### `light_color(color, brightness_factor)`

Return a lighter version of the given color by multiplying its components by the specified brightness factor.

- `color`: The original color, as an (R, G, B) tuple.
- `brightness_factor`: The factor to multiply the color components by (a value between 0 and 1).

## TODO
- `Async version` because for some people just scrolling is not enough ;)

Possible optimizations:

- `Optimize scrolling performance / Memory usage`  
    Right now just make a big framebuffer for long text and scroll it. If memory was a constraint, we could only make the framebuffer 2 letters bigger than the text, and only "scroll inside the view" letter by letter:
    B|erg|h(ain)
- ``Vertical support``, like vertical scrolling (letters would need top->down)
- ``Fonts`` Add support for different character sizes and fonts (which cannot be done with simple framebuf.text)
- ``Graphics functions`` (drawing shapes and images) - everything framebuf can do is simple