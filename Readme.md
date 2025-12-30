# NeoPixel Matrix for MicroPython

The `NeoPixelMatrix` module is a simple library to display text and graphics on a NeoPixel LED matrix using MicroPython. This module provides an easy way to control the LED matrix, including scrolling text, setting colors, and adjusting the brightness. This library was specifically written for an 8x32 WS2812b Matrix and has been tested on ESP32.

Here's a video of the features:

[![Video Tutorial](https://img.youtube.com/vi/OTWfCaKkqZk/0.jpg)](https://www.youtube.com/watch?v=OTWfCaKkqZk)

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
      - [Methods](#methods-1)
  - [NeoPixelMatrixAsync](#neopixelmatrixasync)
    - [Initialization](#initialization-1)
    - [Methods](#methods-2)
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
- 📊 Display progress bars

## Installation

### Using the files

To use the `NeoPixelMatrix` module, simply copy the `neopixel_matrix.py` and `neopixel_matrix_async.py` files to your MicroPython board. If you don't have a matrix attatched, you can use `neopixel_matrix_mock.py` to get an idea of your text in the console.

**Note**: This is the reccomended way of installing the project, as many Micro Controllers don't support more complex file structures, like the one needed in the next Method.

### Installing as a Module

To install the `NeoPixelMatrix` as it's own module, simply copy the `micropython_neopixel_matrix` sub-directory into the root directory of your project / to your MicroPython board (or any other place accessible by your MicroPython script).

**Note**: I have (only) tested this on the RPI Pico 2. (It does work on it)  
But I don't have access to an ESP32 right now, so no guarantee the ESP32 supports this method  -- L7

**Note 2**: by intalling the library like this, you will have to use the following import:

```python
from micropython_neopixel_matrix.neopixel_matrix import NeoPixelMatrix, Color
# Note the added `micropython_neopixel_matrix` namespace!
```

## Usage

Here is an example of how to use the `NeoPixelMatrix` module:

```python
from neopixel_matrix import NeoPixelMatrix, Color # or with the `micropython_neopixel_matrix` namespace, if you are using the library as a module
import time

# Initialize the NeoPixel matrix
PIN = 23 # Replace with whatever pin you are using in your setup
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


### Tips and tricks ###

## Manual refresh

# This will, line by line, change the color of the led matrix
for y in range(np_matrix.height*4):
  np_matrix.line(pos1=(0, y%np_matrix.height), pos2=(32, y%np_matrix.height), color=Color.random())

np_matrix.clear()
time.sleep(1)

# Sometimes you don't want to go line by line, but refresh everything all at once.
# By setting manual_refresh to True, you will have to call np_matrix.show() yourself.
# (This doesn't work with srolling text and the async NeoPixelMatrix class; those will behave as normal)
np_matrix.manual_refresh = True
for y in range(np_matrix.height*4):
  np_matrix.line(pos1=(0, y%np_matrix.height), pos2=(32, y%np_matrix.height), color=Color.random())
np_matrix.show() # only update the actual LED matrix now
np_matrix.manual_refresh = False # Remember to reset everything to the way it was before



# Clear the matrix (again)
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

- `text(self, string:str, x:int=0, y:int=0, color:tuple=Color.RED, center:bool=False)`: Display a given Text on the NeoPixel matrix.
    - `string` : str: The text to display
    **(Optional:)**
    - `x`      : int:                         The x-coordinate of the top-left corner of the Text on the matrix. Defaults to 0.
    - `y`      : int:                         The y-coordinate of the top-left corner of the Text on the matrix. Defaults to 0.
    - `color`  : tuple(r:int, g:int, b:int):  The RGB color of the text. Defaults to Color.RED.
    - `center` : bool:                        If True, the text will be centered on the matrix. Defaults to False.

- `scroll_text(self, string:str, x:int=0, y:int=0, color:tuple=Color.RED, delay:float=0.07, scroll_in:bool=True, scroll_out:bool=True)`: Scroll the given text on the NeoPixel matrix with the specified parameters.
    - `string`     : str:                         The text string to be scrolled.
    **(Optional:)**
    - `x`          : int:                         The initial x-coordinate of the text in the matrix. Defaults to 0.
    - `y`          : int:                         The initial y-coordinate of the text in the matrix. Defaults to 0.
    - `color`      : tuple(r:int, g:int, b:int):  The RGB color of the text. Defaults to Color.RED.
    - `delay`      : float:                       The time delay (in seconds) between each scrolling step. Defaults to 0.07.
    - `scroll_in`  : bool:                        If True, the text will scroll in from the right edge of the matrix. Defaults to True.
    - `scroll_out` : bool:                        If True, the text will scroll out to the left edge of the matrix. Defaults to True.

        Example usage:

        ```python
        np_matrix.scroll_text("Hello, world!", color=Color.GREEN, delay=0.1, scroll_in=True, scroll_out=True)
        ```

 - `draw_progress_bar(progress:int, max_progress:int, color:tuple=Color.RED, margin:int=2, height:int=4)`: Draw a progress bar on the NeoPixel matrix.
    - `progress`     : int:                         The current progress value.
    - `max_progress` : int:                         The maximum progress value.
    **(Optional:)**
    - `color`        : tuple(r:int, g:int, b:int):  The color of the progress bar, as an (R, G, B) tuple. Default is Color.RED.
    - `margin`       : int:                         The margin (in pixels) between the progress bar and the edge of the matrix. Default is 2.
    -` height`       : int:                         The height (in pixels) of the progress bar. Default is 4.

        Example usage:

        ```python
        matrix = NeoPixelMatrix(pin=5, width=32, height=8)
        matrix.draw_progress_bar(50, 100, color=Color.GREEN)
        ```

- `line(pos1: tuple[int, int], pos2: tuple[int, int], color: tuple)`: Draw a line from pos1 to pos2 using the `FrameBuf.line()` function.
    - `pos1`  : tuple(x:int, y:int):         The start position of the line
    - `pos2`  : tuple(x:int, y:int):         The end position of the line
    **(Optional:)**
    - `color` : tuple(r:int, g:int, b:int):  The color of the line, as an (R, G, B) tuple. Default is Color.RED.

- `rect(pos1: tuple[int, int], pos2: tuple[int, int], color: tuple=Color.RED, fill:bool=True)`: Draw a rectangle with the upper-left corner at pos1 and the lower-right corner at pos2.
    - `pos1`  : tuple(x:int, y:int):         The upper-left corner of the rectangle
    - `pos2`  : tuple(x:int, y:int):         The lower-right corner of the rectangle
    **(Optional:)**
    - `color` : tuple(r:int, g:int, b:int):  The color of the rectangle, as an (R, G, B) tuple. Default is Color.RED.
    - `fill`  : bool:                        If True, the rectange will be filled with the given color; if False, only the outline will be drawn. Defaults to True.

- `fill(color)`: Fill the entire matrix with the specified color.

- `show()`: Update the NeoPixel matrix with the current contents of the framebuffer.

- `clear(refresh:bool=True)`: Clear the NeoPixel matrix by setting all pixels to the background color.
    - `refresh` : bool:  If True, the function **wont** call `show()`, reducing the updates to the matrix and thus preventing some potential flickerring


### Color

The `Color` class provides constants and helper functions for working with colors.

#### Constants

| Color Sample | Constant | RGB values |
|--------------|----------|----------- |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(255, 0, 0);"></span>     | `RED`     | `(255, 0, 0)`     |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(0, 255, 0);"></span>     | `GREEN`   | `(0, 255, 0)`     |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(0, 0, 255);"></span>     | `BLUE`    | `(0, 0, 255)`     |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(0, 255, 255);"></span>   | `CYAN`    | `(0, 255, 255)`   |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(255, 255, 0);"></span>   | `YELLOW`  | `(255, 255, 0)`   |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(255, 140, 0);"></span>   | `ORANGE`  | `(255, 140, 0)`   |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(245, 168, 186);"></span> | `PINK`    | `(245, 168, 186)` |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(255, 0, 255);"></span>   | `MAGENTA` | `(255, 0, 255)`   |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(140, 0, 140);"></span>   | `PURPLE`  | `(140, 0, 140)`   |
| <span style="display:inline-block; width: 50px; height: 20px; background-color: rgb(255, 255, 255);"></span> | `WHITE`   | `(255, 255, 255)` |
| (LED off)                                                                                                      | `BLACK`   | `(0, 0, 0)`       |

#### Methods

- `random()`: Return a random color as an (R, G, B) tuple.

- `light_color(color, brightness_factor)`: Return a lighter version of the given color by multiplying its components by the specified brightness factor.
    - `color`: The original color, as an (R, G, B) tuple.
    - `brightness_factor`: The factor to multiply the color components by (a value between 0 and 1).

- `hex_to_rgb(hex_string: str)`: Convert a rgb888 hex string into a 24-bit RGB888 color, represented as a tuple.
    - `hex_string` : str:    The RGB888 hex string

    Return value:
    - `rgb`        : tuple:  The RGB888 color value as a tuple

- `rgb_to_rgb565(rgb:tuple)`: Convert a 24-bit RGB888 color to a 16-bit RGB565 color.
    - `rgb`    : tuple:  The RGB color value as a tuple (r, g, b).

    Return value:
    - `rgb565` : int:    The 16-bit RGB565 color value.

- `rgb565_to_rgb888(self, color:int)`: Convert a 16-bit RGB565 color to a 24-bit RGB888 color and apply brightness.
    - `color` : int:    The RGB565 color value.

    Return value:
    - `rgb`   : tuple:  The RGB888 color value after brightness adjustment.


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
from neopixel_matrix_async import NeoPixelMatrixAsync
from neopixel_matrix import Color

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
from neopixel_matrix_mock import MockNeoPixelMatrix
from neopixel_matrix import Color

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
