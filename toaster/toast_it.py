import time
from neopixel_matrix import NeoPixelMatrix, Color
from neopixel_matrix_async import NeoPixelMatrixAsync
from neopixel_matrix_mock import MockNeoPixelMatrixAsync
from toaster.utils import format_ticks
import uasyncio as asyncio
import random
import machine


machine.freq(240000000)

DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
WIDTH = 32
HEIGHT = 8
DIRECTION = NeoPixelMatrix.HORIZONTAL
SLEEP_TIME = 1000
BRIGHTNESS= 0.4

HEATING_TIME = 80
start_time = time.ticks_ms()

async def timer(matrix, sec=10, offset=0):
        for _ in range(sec):
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time) - (offset*1000)

            formatted_time = format_ticks(elapsed_time)
            await matrix.text(formatted_time, center=True)
            await asyncio.sleep(1)


def elapsed_time():
    return time.ticks_diff(time.ticks_ms(), start_time) // 1000

async def toast_display():
    matrix = NeoPixelMatrixAsync(23 ,32, 8)

    await matrix.scroll_text("Happy Toasting!", delay=0)
    await matrix.scroll_text("Heating.", delay=0.01)
    while elapsed_time() < HEATING_TIME:
       
        progress_color = Color.GREEN
        if elapsed_time() > 25:
            progress_color = (255,180,0) # Yellow on my machine
        elif elapsed_time() > 60:
            progress_color = Color.RED

        await matrix.draw_progress_bar(progress=elapsed_time(), max_progress=80, color=progress_color)
        await asyncio.sleep(
            random.randint(2,10)
            )
        if elapsed_time() > 80:
            break
        await timer(
            matrix,
            random.randint(3,10)
            )
        if elapsed_time() > 80:
            break
        await matrix.scroll_text("Heating", delay=0.02)
        asyncio.sleep(1)

    # Now is HOT
    await matrix.text("HOT", center=True)
    while 1:
        await matrix.text("HOT", center=True)
        await asyncio.sleep(
            random.randint(2,10)
            )
        await timer(
            matrix,
            random.randint(3,15),
            offset=HEATING_TIME
            )

asyncio.run(
   #test_progress()
   toast_display()
)

