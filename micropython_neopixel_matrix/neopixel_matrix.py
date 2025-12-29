# -*- coding: utf-8 -*-
# NeoPixel Matrix for MicroPython
# Used with ESP32 and 8x32 WS2812b LED matrix
# neopixel_matrix.py


# Fixes by L7:
#   - Specified argument- and return Types
#   - Now using the `NeoPixelMatrix.rgb_to_rgb565` function everywhere
#   - added the `NeoPixelMatrix.line` and `NeoPixelMatrix.rect` functions
#   - added a "refresh" argument to `NeoPixelMatrix.clear()` and replaced some `NeoPixelMatrix.fill(self.bg_color)` calls with `NeoPixelMatrix.clear(refresh=False)`
#   - added the `NeoPixelMatrix.manual_refresh`: setting it to True makes all "drawing functions" not call `NeoPixelMatrix.show()` (except for `NeoPixelMatrix.scroll_text()`), allowing for drawing without "screen" updates
#   - added more colours (I found them useful for the project I was working on, but feel free to remove them!)

import gc
import utime
import machine
import neopixel
import framebuf
import time
import random
#from utils.timed_func import time_acc_function, timed_function


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)

    PINK = (245, 168, 186)
    AQUA = (85, 255, 255)
    ORANGE = (255, 140, 0)
    PURPLE = (140, 0, 140)

    @staticmethod
    def random():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    @staticmethod
    def light_color(color, brightness_factor):
        return tuple(int(x * brightness_factor) for x in color)


class NeoPixelMatrix:
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, pin:int, width:int, height:int, direction:int=HORIZONTAL, brightness:float=1.0, bg_color:tuple=Color.BLACK) -> None:
        self.width = width
        self.height = height

        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, width * height)
        self.fb = framebuf.FrameBuffer(
            bytearray(width * height * 2), width, height, framebuf.RGB565)
        self.fb_width = width

        self.direction = direction
        # Ensure the brightness value is within the range [0, 1]
        self.brightness = max(0, min(1, brightness))
        self.bg_color = bg_color

        self.manual_refresh = False

    def _transform_coordinates(self, x:int, y:int) -> tuple: # Doesnt work for me: it just flips everything on it's head
        """
        Transform the given x and y coordinates according to the matrix direction.
        """

        if self.direction == NeoPixelMatrix.HORIZONTAL:
            x = self.width - 1 - x
        elif self.direction == NeoPixelMatrix.VERTICAL:
            y = self.height - 1 - y
        return x, y

    def _rgb565_to_rgb888(self, color:int) -> tuple:
        """
        Convert a 16-bit RGB565 color to a 24-bit RGB888 color and apply brightness.

        Args:
            color (int): The RGB565 color value.

        Returns:
            tuple: The RGB888 color value after brightness adjustment.
        """
        if color is None:
            return 0, 0, 0

        # convert 16-bit RGB565 to 24-bit RGB888
        r = ((color >> 11) & 0x1F) << 3
        g = ((color >> 5) & 0x3F) << 2
        b = (color & 0x1F) << 3

        # apply brightness
        r = int(r * self.brightness)
        g = int(g * self.brightness)
        b = int(b * self.brightness)

        return r, g, b

    @staticmethod
    def rgb_to_rgb565(rgb:tuple) -> int:
        """
        Convert a 24-bit RGB888 color to a 16-bit RGB565 color.
    
        Args:
            rgb (tuple): The RGB color value as a tuple (r, g, b).
    
        Returns:
            int: The 16-bit RGB565 color value.
        """
        r, g, b = rgb
        return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)


    def _get_text_width(self, string:str) -> int:
        char_width, char_height = 8, 8  # Assuming each character is 8x8 pixels
        return len(string) * char_width

    def _center_text(self, string:str) -> int:
        text_width = self._get_text_width(string)
        if text_width > self.width:
            print("ATTENTION: Text is too long to be centered on the screen.")
            return 0
        return (self.width - text_width) // 2

    #@timed_function
    def _update_np_from_fb(self) -> None:
        """
        Update the NeoPixel matrix with the current contents of the framebuffer.
        
        This method reads the pixel colors from the framebuffer, applies brightness adjustments,
        and sets the corresponding NeoPixel matrix pixels to the transformed colors.
        """
        gc.collect()
        counter = 0
        self.np.fill(self.bg_color)
        for w in reversed(range(self.width)):
            # Determine the row iteration order based on whether the column is even or odd
            if w % 2 == 0:
                row_order = reversed(range(self.height))
            else:
                row_order = range(self.height)

            for h in row_order:
                x, y = self._transform_coordinates(w, h)
                rgb565 = self.fb.pixel(x, y)
                rgb888_pixel = self._rgb565_to_rgb888(rgb565)

                # Only update non-bg-color pixels; makes the display update faster
                if rgb888_pixel != self.bg_color:
                    self.np[counter] = rgb888_pixel

                counter += 1

    def _draw_text_to_buffer(self, string:str, x:int, y:int, color:tuple, buffer) -> None:
        """
        Draw the given text string to the specified buffer at the given x and y coordinates.
        """
        buffer.text(string, x, y, self.rgb_to_rgb565(color))

    def _update_framebuffer_size(self, fb_width:int) -> None:
        """
        Update the framebuffer size if the given width is different from the current framebuffer width.
        """
        if self.fb_width != fb_width:
            self.fb = framebuf.FrameBuffer(
                bytearray(fb_width * self.height * 2), fb_width, self.height, framebuf.RGB565)
            self.fb_width = fb_width

    def fill(self, color:tuple) -> None:
        self.fb.fill(self.rgb_to_rgb565(color))

    def line(self, pos1: tuple, pos2: tuple, color: tuple) -> None:
        """Please input pos1 & pos2 as tuple(x: int, y: int) - L7"""

        self.fb.line(pos1[0], pos1[1], pos2[0], pos2[1], self.rgb_to_rgb565(color))
        if not self.manual_refresh: self.show()

    def rect(self, pos1: tuple, pos2: tuple, color: tuple, fill:bool=True) -> None:
        """Please input pos1 & pos2 as tuple(x: int, y: int) - L7"""
        self.rgb_to_rgb565(color)
        self.fb.poly(0,0, bytearray([pos1[0],pos1[1], pos2[0],pos1[1], pos2[0],pos2[1], pos1[0],pos2[1]]), self.rgb_to_rgb565(color), fill)

        if not self.manual_refresh: self.show()

    def show(self) -> None:
        self._update_np_from_fb()
        self.np.write()

    def clear(self, refresh: bool = True) -> None:
        self.fill(self.bg_color)
        if refresh and not self.manual_refresh:
            self.show()

    def text(self, string:str, x:int=0, y:int=0, color:tuple=Color.RED, center:bool=False) -> None:
        text_width = self._get_text_width(string)
        fb_width = max(text_width, self.width)

        if center:
            x = self._center_text(string)

        # Update the framebuffer size if its width doesn't match the calculated width
        self._update_framebuffer_size(fb_width)

        # Clear the framebuffer before drawing new text
        self.clear(refresh=False)
        self._draw_text_to_buffer(string, x, y , color, self.fb)
        if not self.manual_refresh: self.show()


    def _get_scroll_text_range(self, string:str, x:int, y:int, color:tuple, scroll_in:bool, scroll_out:bool) -> int:
        """
        Calculate and return the framebuffer width, starting x-coordinate, and scroll range
        for scrolling the given text on the NeoPixel matrix.

        Returns:
                - scroll_range (int): The range of pixels for which the text will be scrolled.
        """

        text_width = self._get_text_width(string)

        if scroll_in:
            fb_width = text_width + self.width  # all text outside the FB
            x = fb_width - text_width  # start at the right edge
        else:
            fb_width = max(text_width, self.width)

        self._update_framebuffer_size(fb_width)

        self.clear(refresh=False)
        self._draw_text_to_buffer(string, x, y, color, self.fb)

        scroll_range = fb_width - self.width  # will stop at the left of the matrix
        if scroll_out:
            scroll_range += self.width  # will go on to get out to the left

        return scroll_range


    def scroll_text(self, string:str, x:int=0, y:int=0, color:tuple=Color.RED, delay:float=0.07, scroll_in:bool=True, scroll_out:bool=True) -> None:
        """
        Scroll the given text on the NeoPixel matrix with the specified parameters.

        Args:
            string (str): The text string to be scrolled.
            x (int, optional): The initial x-coordinate of the text in the matrix. Defaults to 0.
            y (int, optional): The initial y-coordinate of the text in the matrix. Defaults to 0.
            color (tuple, optional): The RGB color of the text. Defaults to Color.RED.
            delay (float, optional): The time delay (in seconds) between each scrolling step. Defaults to 0.07.
            scroll_in (bool, optional): If True, the text will scroll in from the right edge of the matrix. Defaults to True.
            scroll_out (bool, optional): If True, the text will scroll out to the left edge of the matrix. Defaults to True.

        Usage:
            np_matrix.scroll_text("Hello, world!", color=Color.GREEN, delay=0.1, scroll_in=True, scroll_out=True)
        """
        scroll_range = self._get_scroll_text_range(
            string, x=x, y=y, color=color, scroll_in=scroll_in, scroll_out=scroll_out)
        for _ in range(scroll_range):
            self.fb.scroll(-1, 0)
            self.show()
            time.sleep(delay)
            
    
    def draw_progress_bar(self, progress:int, max_progress:int, color:tuple=Color.RED, margin:int=2, height:int=4) -> None:
        """
        Draw a progress bar on the NeoPixel matrix.

        Parameters:
        - progress (int): The current progress value.
        - max_progress (int): The maximum progress value.
        - color (tuple): The color of the progress bar, as an (R, G, B) tuple. Default is Color.RED.
        - margin (int): The margin (in pixels) between the progress bar and the edge of the matrix. Default is 2.
        - height (int): The height (in pixels) of the progress bar. Default is 4.

        Example:
            matrix = NeoPixelMatrix(pin=5, width=32, height=8)
            matrix.draw_progress_bar(50, 100, color=Color.GREEN)
        """
        #self._get_progress_bar(progress, max_progress, margin, height, color)
        max_width = self.width - (2*margin)
        step = max_width / max_progress
        current_width = round(step * progress)

        #self.fill(self.bg_color) # clear does flickering       # -- because of the .show() call! - L7
        # Fix:
        self.clear(refresh=False)
        self.fb.fill_rect(2,margin,current_width, height, self.rgb_to_rgb565(color))
        self.fb.rect(2,margin,max_width, height, self.rgb_to_rgb565(color))
        if not self.manual_refresh: self.show()
