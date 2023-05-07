# NeoPixel Matrix for MicroPython

The `NeoPixelMatrix` module is a simple library to display text and graphics on a NeoPixel LED matrix using MicroPython. This module provides an easy way to control the LED matrix, including scrolling text, setting colors, and adjusting the brightness. This library was specifically written for an 8x32 WS2812b Matrix and has been tested on ESP32.


## Table of Contents

- [NeoPixel Matrix for MicroPython](#neopixel-matrix-for-micropython)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [API Reference](#api-reference)
    - [`NeoPixelMatrix`](#neopixelmatrix)
      - [Initialization](#initialization)
      - [Methods](#methods)
    - [Color](#color)
      - [Constants](#constants)
      - [`random()`](#random)
      - [`light_color(color, brightness_factor)`](#light_colorcolor-brightness_factor)
  - [NeoPixelMatrixAsync](#neopixelmatrixasync)
    - [Initialization](#initialization-1)
    - [Methods](#methods-1)
    - [Example Usage](#example-usage)
  - [MockNeoPixelMatrix](#mockneopixelmatrix)
    - [Initialization](#initialization-2)
    - [Example Usage](#example-usage-1)
    - [Console Output](#console-output)
  - [TODO](#todo)

## Features

- 🔤 Display text in multiple colors
- ↔️ Scrolling text horizontally
- 💡 Control the brightness of the "display"
- 🔄 ~~Support for both horizontal and vertical LED matrices~~ [Badly impemented]
- 🌈 Predefined color constants and helper functions
- ⏱️ Async support for non-blocking matrix control

## Installation

To use the `NeoPixelMatrix` module, simply copy the `neopixel_matrix.py` and `neopixel_matrix_async.py` files to your MicroPython board. If you don't have a matrix attatched, you can use `neopixel_matrix_mock.py` to get an idea of your text in the console.

## Usage

Here is an example of how to use the `NeoPixelMatrix` module:

```python
from neopixel_matrix import NeoPixelMatrix, Color
import time

# Initialize the NeoPixel matrix
PIN = 23
np_matrix = NeoPixelMatrix(pin=PIN, width=32, height=8, direction=NeoPixelMatrix.HORIZONTAL, brightness=1.0)

# Display text on the matrix
np_matrix.text("Hello, world!", color=Color.GREEN)
time.sleep(1)

# Scroll text on the matrix
np_matrix.scroll_text("Scrolling text!", color=Color.YELLOW, delay=0.1, scroll_in=True, scroll_out=True)

# Fill the entire matrix with a specific color
np_matrix.fill(Color.BLUE)
time.sleep(1)

# Clear the matrix
np_matrix.clear()
```

## API Reference
### `NeoPixelMatrix`

The `NeoPixelMatrix` class provides methods for controlling the NeoPixel matrix.

#### Initialization

```python
np_matrix = NeoPixelMatrix(pin, width, height, direction=HORIZONTAL, brightness=1.0, bg_color=Color.BLACK)
```

- `pin` (int): The GPIO pin connected to the data pin of the NeoPixel matrix.
- `width` (int): The width of the NeoPixel matrix.
- `height` (int): The height of the NeoPixel matrix.
- `direction` (int, optional): The direction of the LED matrix. Use `NeoPixelMatrix.HORIZONTAL` for horizontal matrices or `NeoPixelMatrix.VERTICAL` for vertical matrices. Defaults to `NeoPixelMatrix.HORIZONTAL`.
- `brightness` (float, optional): The initial brightness of the matrix (0 to 1). Defaults to 1.0.
- `bg_color` (tuple, optional): The background color of the matrix as an RGB tuple. Defaults to `Color.BLACK`.

#### Methods

- `text(string, x=0, y=0, color=Color.RED, center=False)`: Display the given text on the NeoPixel matrix.

- `scroll_text(string, x=0, y=0, color=Color.RED, delay=0.07, scroll_in=True, scroll_out=True)`:   
  Scroll the given text on the NeoPixel matrix with the specified parameters.
    - `string` (str): The text string to be scrolled.
    - `x` (int, optional): The initial x-coordinate of the text in the matrix. Defaults to 0.
    - `y` (int, optional): The initial y-coordinate of the text in the matrix. Defaults to 0.
    - `color` (tuple, optional): The RGB color of the text. Defaults to Color.RED.
    - `delay` (float, optional): The time delay (in seconds) between each scrolling step. Defaults to 0.07.
    - `scroll_in` (bool, optional): If True, the text will scroll in from the right edge of the matrix. If False, the text will begin at the specified x-coordinate (0 by default). Defaults to True.
    - `scroll_out` (bool, optional): If True, the text will continue scrolling until it exits the left edge of the matrix. If False, the text will stop scrolling once its right edge reaches the left edge of the matrix. Defaults to True.

        Example usage:

        ```python
        np_matrix.scroll_text("Hello, world!", color=Color.GREEN, delay=0.1, scroll_in=True, scroll_out=True)
        ```

        In this example, the text "Hello, world!" will scroll in from the right edge of the matrix with a delay of 0.1 seconds between each scrolling step. The text will be displayed in green and will continue scrolling until it exits the left edge of the matrix.  

- `fill(color)`: Fill the entire matrix with the specified color.

- `show()`: Update the NeoPixel matrix with the current contents of the framebuffer.

- `clear()`: Clear the NeoPixel matrix by setting all pixels to the background color.


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




## NeoPixelMatrixAsync

The `NeoPixelMatrixAsync` class is a subclass of the `NeoPixelMatrix` class, which provides asynchronous versions of the methods for controlling the NeoPixel matrix. This allows you to perform non-blocking matrix operations, such as scrolling text or updating the display, while running other tasks concurrently using `uasyncio`.

### Initialization

```python
from neopixel_matrix_async import NeoPixelMatrixAsync

np_matrix_async = NeoPixelMatrixAsync(pin=18, width=32, height=8, direction=NeoPixelMatrix.HORIZONTAL, brightness=1.0)
```

### Methods

- `async def show()`: Update the NeoPixel matrix with the current contents of the framebuffer asynchronously.

- `async def text(string, x=0, y=0, color=Color.RED, center=False)`: Display the given text on the NeoPixel matrix asynchronously.

- `async def scroll_text(string, x=0, y=0, color=Color.RED, delay=0.07, scroll_in=True, scroll_out=True)`: Scroll the given text on the NeoPixel matrix with the specified parameters asynchronously.

### Example Usage

```python
import uasyncio as asyncio
from neopixel_matrix_async import NeoPixelMatrixAsync, Color

np_matrix_async = NeoPixelMatrixAsync(pin=23, width=32, height=8, direction=NeoPixelMatrix.HORIZONTAL, brightness=1.0)

async def main():
    await np_matrix_async.scroll_text("Hello, world!", color=Color.GREEN, delay=0.1, scroll_in=True, scroll_out=True)

asyncio.run(main())
```

In this example, the text "Hello, world!" will scroll in from the right edge of the matrix with a delay of 0.1 seconds between each scrolling step. The text will be displayed in green and will continue scrolling until it exits the left edge of the matrix. The scrolling operation will be performed asynchronously, allowing other tasks to run concurrently.


## MockNeoPixelMatrix

The `MockNeoPixelMatrix` class is a subclass of the `NeoPixelMatrix` class that simulates a NeoPixel matrix by printing the matrix content to the console. Instead of updating the NeoPixel hardware, it overrides the `show()` method to display the matrix in the console using '#' characters for colored pixels and '-' characters for background pixels. This can be useful for testing and debugging purposes when a physical NeoPixel matrix is not available.

### Initialization

```python
from neopixel_matrix import MockNeoPixelMatrix

mock_matrix = MockNeoPixelMatrix(width=32, height=8, direction=NeoPixelMatrix.HORIZONTAL, brightness=1.0)
```

### Example Usage

```python
mock_matrix.text('Hello World', 0, 0, color=Color.RED)
```

In this example, the text "Hello World" will be displayed on the simulated NeoPixel matrix in the console. The console output will represent colored pixels with '#' characters and background pixels with '-' characters.

### Console Output

```
-##--##-----------###-----###---
-##--##------------##------##---
-##--##---####-----##------##---
-######--##--##----##------##---
-##--##--######----##------##---
-##--##--##--------##------##---
-##--##---#####---####----####--
--------------------------------
```


## TODO

Possible optimizations and enhancements for future development:

- 🚀 `Optimize scrolling performance / Memory usage`  
    The current implementation creates a large framebuffer for long text and scrolls it. If memory was a constraint, we could make the framebuffer only 2 letters bigger than the text and scroll letter by letter "inside the view":
    B|erg|h(ain)

- 📏 `Vertical support`  
    Add support for vertical scrolling, where letters would need to be displayed top-to-bottom.

- 🖋️ `Fonts`  
    Add support for different character sizes and fonts, which cannot be achieved with the simple `framebuf.text` method alone.

- 🎨 `Graphics functions`  
    Implement drawing shapes and images using the capabilities of the `framebuf` module or other graphics libraries.
