# -*- coding: utf-8 -*-
# NeoPixel Matrix for MicroPython
# neo_matrix.py

import machine
import neopixel
import framebuf

class NeoPixelMatrix:
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, pin, width, height, direction=HORIZONTAL):
        self.width = width
        self.height = height
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, width * height)
        self.fb = framebuf.FrameBuffer(bytearray(width * height * 2), width, height, framebuf.RGB565)
        self.direction = direction

    def _transform_coordinates(self, x, y):
        if self.direction == NeoPixelMatrix.HORIZONTAL:
            x = self.width - 1 - x
        elif self.direction == NeoPixelMatrix.VERTICAL:
            y = self.height - 1 - y
        return x, y

    def _rgb565_to_rgb888(self, rgb565):
        r = (rgb565 >> 11) & 0x1F
        g = (rgb565 >> 5) & 0x3F
        b = rgb565 & 0x1F
        return (r << 3, g << 2, b << 3)



    def _update_np_from_fb(self):
        counter = 0
        for w in reversed(range(self.width)):
            if w % 2 == 0:
                for h in reversed(range(self.height)):
                    x, y = self._transform_coordinates(w, h)
                    rgb565 = self.fb.pixel(x, y)
                    self.np[counter] = self._rgb565_to_rgb888(rgb565)
                    counter += 1
            else:
                for h in range(self.height):
                    x, y = self._transform_coordinates(w, h)
                    rgb565 = self.fb.pixel(x, y)
                    self.np[counter] = self._rgb565_to_rgb888(rgb565)
                    counter += 1


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

        r, g, b = color
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        self.fb.text(string, x, y, rgb565)

    def scroll(self, dx, dy):
        self.fb.scroll(dx, dy)
        self.show()


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
