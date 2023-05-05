# neopixels_rainbow.py

import machine
import neopixel

class Rainbow:
    """
    Rainbow class to generate rainbow colors

    :param pixels: NeoPixel object
    :param steps: number of steps in the rainbow
    :param sleep_ms: sleep time in milliseconds
    :param brightness: brightness of the rainbow
    """
    
    def __init__(self, pixels, steps=300, sleep_ms=5, brightness=1.0 ):
        self.pixels = pixels
        self.brightness = brightness
        self.steps = steps
        self.sleep_ms = sleep_ms
        self.counter = 0

    @staticmethod
    def hsl_to_rgb(h, s, l):
        def hue_to_rgb(p, q, t):
            if t < 0: t += 1
            if t > 1: t -= 1
            if t < 1/6: return p + (q - p) * 6 * t
            if t < 1/2: return q
            if t < 2/3: return p + (q - p) * (2/3 - t) * 6
            return p

        if s == 0:
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = hue_to_rgb(p, q, h + 1/3)
            g = hue_to_rgb(p, q, h)
            b = hue_to_rgb(p, q, h - 1/3)

        return int(r * 255), int(g * 255), int(b * 255)

    def generate_rainbow(self):
        for i in range(self.steps):
            hue = i / self.steps
            saturation = 1
            lightness = self.brightness * 0.5
            r, g, b = self.hsl_to_rgb(hue, saturation, lightness)
            yield (r, g, b)

    def fill(self):
        for color in self.generate_rainbow():
            pixels.fill(color)
            pixels.write()
            machine.lightsleep(self.sleep_ms)


if __name__ == '__main__':
    # Pin = 23
    # Device is a WS2812B

    p = machine.Pin(23, machine.Pin.OUT)
    pixels = neopixel.NeoPixel(p, 256)
    rainbow = Rainbow(pixels, steps=300)
    rainbow.fill()
