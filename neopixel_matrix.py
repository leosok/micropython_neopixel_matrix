# -*- coding: utf-8 -*-
# NeoPixel Matrix for MicroPython
# Used with ESP32 and 8x32 WS2812b LED matrix
# neopixel_matrix.py

import gc
import machine
import neopixel
import framebuf
import time
import random
from timed_func import timed_function

class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WHITE = (255, 255, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    BLACK = (0, 0, 0)

    @staticmethod
    def random():
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    @staticmethod
    def light_color(color, brightness_factor):
        return tuple(int(x * brightness_factor) for x in color)


class NeoPixelMatrix:
    HORIZONTAL = 0
    VERTICAL = 1

    
    def __init__(self, pin, width, height, direction=HORIZONTAL, brightness=1.0, bg_color=Color.BLACK):
        self.width = width
        self.height = height
    
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, width * height)                
        self.fb = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)
        self.fb_width = width
       
        self.direction = direction
        self.brightness = max(0, min(1, brightness))  # Ensure the brightness value is within the range [0, 1]
        self.bg_color = bg_color


    def _transform_coordinates(self, x, y):
        if self.direction == NeoPixelMatrix.HORIZONTAL:
            x = self.width - 1 - x
        elif self.direction == NeoPixelMatrix.VERTICAL:
            y = self.height - 1 - y
        return x, y


    def _rgb565_to_rgb888(self, color):
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

    def _get_text_width(self, string):
        char_width, char_height = 8, 8  # Assuming each character is 8x8 pixels
        return len(string) * char_width

    def _center_text(self, string):
        text_width = self._get_text_width(string)
        if text_width > self.width:
            print("ATTENTION: Text is too long to be centered on the screen.")
            return 0
        return (self.width - text_width) // 2


    @timed_function
    def _update_np_from_fb(self):
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
    

    def _draw_text_to_buffer(self, string, x, y, color, buffer):
        r, g, b = color
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        buffer.text(string, x, y, rgb565)

    
    def _update_framebuffer_size(self, fb_width):
        if self.fb_width != fb_width:
            self.fb = framebuf.FrameBuffer(bytearray(fb_width * self.height * 2), fb_width, self.height, framebuf.RGB565)
            self.fb_width = fb_width



    def fill(self, color):
        r, g, b = color
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        self.fb.fill(rgb565)

    def show(self):
        self._update_np_from_fb()
        self.np.write()

    def clear(self):
        self.fill(self.bg_color)
        self.show()


    def text(self, string, x=0, y=0, color=Color.RED, center=False):
        text_width = self._get_text_width(string)
        fb_width = max(text_width, self.width)

        if center:
            x = self._center_text(string)

        # Update the framebuffer size if its width doesn't match the calculated width
        self._update_framebuffer_size(fb_width)

        self.fill(self.bg_color)  # Clear the framebuffer before drawing new text
        self._draw_text_to_buffer(string, x, y, color, self.fb)
        self.show()

    @timed_function
    def scroll(self, delay=0.1, scroll_out=True):
        fb_width = self.fb_width
        if scroll_out:
            scroll_range =  fb_width + self.width
        else:
            scroll_range = fb_width - self.width + 1
        for i in range(scroll_range):
            self.fb.scroll(-1, 0)
            self.show()
            time.sleep(delay)

