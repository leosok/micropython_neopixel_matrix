# -*- coding: utf-8 -*-
# NeoPixel Matrix for MicroPython
# neo_matrix.py

import machine
import neopixel

class NeoPixelMatrix:
    HORIZONTAL = 0
    VERTICAL = 1

    def __init__(self, pin, width, height):
        self.width = width
        self.height = height
        self.pin = machine.Pin(pin, machine.Pin.OUT)
        self.np = neopixel.NeoPixel(self.pin, width * height)
        self.flip_direction = NeoPixelMatrix.HORIZONTAL

    def set_flip(self, direction):
        if direction in [NeoPixelMatrix.HORIZONTAL, NeoPixelMatrix.VERTICAL]:
            self.flip_direction = direction
        else:
            raise ValueError("Invalid direction. Use NeoPixelMatrix.HORIZONTAL or NeoPixelMatrix.VERTICAL.")

    def _transform_coordinates(self, x, y):
        if self.flip_direction == NeoPixelMatrix.HORIZONTAL:
            x = self.width - 1 - x
        elif self.flip_direction == NeoPixelMatrix.VERTICAL:
            y = self.height - 1 - y
        return x, y

    def set_pixel(self, x, y, color):
        x, y = self._transform_coordinates(x, y)
        if 0 <= x < self.width and 0 <= y < self.height:
            index = x + y * self.width
            self.np[index] = color

    def fill(self, color):
        self.np.fill(color)

    def show(self):
        self.np.write()

    def clear(self):
        self.fill((0, 0, 0))
        self.show()


if __name__ == '__main__':
    from machine import Pin
    from time import sleep
    #from neopixel_matrix import NeoPixelMatrix

    # Configure the pin number, width, and height
    DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
    WIDTH = 32
    HEIGHT = 8
    DIRECTION = NeoPixelMatrix.HORIZONTAL

    matrix = NeoPixelMatrix(DATA_PIN, WIDTH, HEIGHT)

    # Fill the entire matrix with a single color
    matrix.fill((255, 0, 0))  # Red
    matrix.show()
    sleep(1)

    # Clear the matrix
    matrix.clear()

    # Set flip direction to horizontal
    matrix.set_flip(NeoPixelMatrix.HORIZONTAL)

    # Set individual pixels to different colors
    matrix.set_pixel(0, 0, (255, 0, 0))  # Red
    matrix.set_pixel(1, 0, (0, 255, 0))  # Green
    matrix.set_pixel(2, 0, (0, 0, 255))  # Blue
    matrix.show()
    sleep(1)

    # Clear the matrix
    matrix.clear()

    # Set flip direction to vertical
    matrix.set_flip(NeoPixelMatrix.VERTICAL)

    # Set individual pixels to different colors
    matrix.set_pixel(0, 0, (255, 0, 0))  # Red
    matrix.set_pixel(1, 0, (0, 255, 0))  # Green
    matrix.set_pixel(2, 0, (0, 0, 255))  # Blue
    matrix.show()
    sleep(1)

    # Clear the matrix
    matrix.clear()
