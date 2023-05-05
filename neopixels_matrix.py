# -*- coding: utf-8 -*-
# NeoPixel Matrix for MicroPython
# neo_matrix.py

import machine
import neopixel
import framebuf
import time

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

    
    def __init__(self, pin, width, height, direction=HORIZONTAL, brightness=1.0):
        self.width = width
        self.height = height
    
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, width * height)                
        self.fb = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)
        self.fb_width = width
       
        self.direction = direction
        self.brightness = max(0, min(1, brightness))  # Ensure the brightness value is within the range [0, 1]


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

    def _update_np_from_fb(self, dx=0, dy=0):
        counter = 0
        for w in reversed(range(self.width)):
            if w % 2 == 0:
                for h in reversed(range(self.height)):
                    x, y = self._transform_coordinates(w, h)
                    rgb565 = self.fb.pixel(x + dx, y + dy)
                    self.np[counter] = self._rgb565_to_rgb888(rgb565)
                    counter += 1
            else:
                for h in range(self.height):
                    x, y = self._transform_coordinates(w, h)
                    rgb565 = self.fb.pixel(x + dx, y + dy)
                    self.np[counter] = self._rgb565_to_rgb888(rgb565)
                    counter += 1

   

    def _draw_text_to_buffer(self, string, x, y, color, buffer):
        r, g, b = color
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        buffer.text(string, x, y, rgb565)


    def fill(self, color):
        r, g, b = color
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        self.fb.fill(rgb565)

    def show(self):
        self._update_np_from_fb()
        self.np.write()

    def clear(self):
        self.fill((0, 0, 0))
        self.show()


    def text(self, string, x, y, color):
        text_width = self._get_text_width(string)
        fb_width = max(text_width, self.width)

        # Update the framebuffer size if its width doesn't match the calculated width
        if self.fb_width != fb_width:
            self.fb = framebuf.FrameBuffer(bytearray(fb_width * self.height * 2), fb_width, self.height, framebuf.RGB565)
            self.fb_width = fb_width

        self.fill((0, 0, 0))  # Clear the framebuffer before drawing new text
        self._draw_text_to_buffer(string, x, y, color, self.fb)
        self.show()


    # def scroll(self, delay=0.1):
    #     fb_width = self.fb_width
    #     for i in range(fb_width - self.width + 1):
    #         print(f"i: {i}")
    #         self._update_np_from_fb(i, 0)
    #         self.show()
    #         time.sleep(delay)

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

class MockNeoPixelMatrix(NeoPixelMatrix):
    def __init__(self, width, height, direction=NeoPixelMatrix.HORIZONTAL):
        self.width = width
        self.height = height
        self.direction = direction
        self.fb = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)

    def show(self):
        self._update_np_from_fb()
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                # index = x + y * self.width
                r, g, b = self._rgb565_to_rgb888(self.fb.pixel(x, y))
                if r > 127 or g > 127 or b > 127:
                    row += '#'
                else:
                    row += '.'
            print(row)
