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

counter = 0
fbuf.text('HOT', 5, 1, 1)

for w in reversed(range(DISPLAY_WIDTH)):
    for h in reversed(range(DISPLAY_HEIGHT)):
        # if we are in a even line, we need to go backwards
        if w % 2 == 0:
            pixel = fbuf.pixel(w, (7 - h)) or 0
        else:
            pixel = fbuf.pixel(w, h) or 0
        pval = (pixel * 20)
        n[counter] = (pval, 0, 0)
        print(h if pixel == 1 else ' ', end=' ')
        counter += 1
    n.write()
    print()

# #---------------------