import neopixel
import machine
import framebuf

import random
# 32 LED strip connected to X8.
p = machine.Pin(23, machine.Pin.OUT)
n = neopixel.NeoPixel(p, 256)


n.fill((0,0,0))
n.write()


# FrameBuffer needs 2 bytes for every RGB565 pixel
buffer = bytearray(100 * 10 * 2)
fbuf = framebuf.FrameBuffer(buffer, 32, 8, framebuf.MVLSB)


DISPLAY_WIDTH = 32
DISPLAY_HEIGHT = 8


DISPLAY_WIDTH = 32
DISPLAY_HEIGHT = 8
TEXT = 'TOAST'

counter = 0

def draw_text_to_fbuf(text, x):
    fbuf.fill(0)
    fbuf.text(text, x, 1, 1)

text_x = 5
text_width = 3 * 8  # Assuming each character is 6 pixels wide
draw_text_to_fbuf(TEXT, text_x)

def scroll_framebuffer_left(fbuf):
    for h in range(DISPLAY_HEIGHT):
        for w in range(DISPLAY_WIDTH - 1):
            pixel = fbuf.pixel(w + 1, h) or 0
            fbuf.pixel(w, h, pixel)
        fbuf.pixel(DISPLAY_WIDTH - 1, h, 0)

while True:
    for w in reversed(range(DISPLAY_WIDTH)):
        for h in reversed(range(DISPLAY_HEIGHT)):
            # if we are on an even line, we need to go backwards
            if w % 2 == 0:
                pixel = fbuf.pixel(w, (7 - h)) or 0
            else:
                pixel = fbuf.pixel(w, h) or 0
            pval = (pixel * 20)
            n[counter] = (pval, 0, 0)
            counter += 1
        n.write()
        #print()
    counter = 0

    # Scroll the frame buffer and update the starting position of the text
    scroll_framebuffer_left(fbuf)
    text_x -= 1

    if text_x + text_width <= 0:  # Check if the text is completely out of the display
        text_x = DISPLAY_WIDTH - 1  # Reset the text starting position
    draw_text_to_fbuf(TEXT, text_x)

    #machine.sleep(10)
