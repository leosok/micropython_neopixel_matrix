import time
from neopixel_matrix import NeoPixelMatrix
from neopixel_matrix_async import NeoPixelMatrixAsync
from neopixel_matrix_mock import MockNeoPixelMatrixAsync
from toaster.utils import format_ticks
import uasyncio as asyncio
import random


DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
WIDTH = 32
HEIGHT = 8
DIRECTION = NeoPixelMatrix.HORIZONTAL
SLEEP_TIME = 1000
BRIGHTNESS= 0.4
start_time = time.ticks_ms()

async def timer(matrix, sec=10):
        for _ in range(sec):
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            formatted_time = format_ticks(elapsed_time)
            await matrix.text(formatted_time, center=True)
            await asyncio.sleep(1)

async def draw_progress_bar(matrix, now, max):
    margin = 2
    height = 4
    max_width = matrix.width - (2*margin)
    step = max_width / max
    current_width = round(step * now)
    print(f"Drawing Progressbar with width: {current_width} ")

    matrix.clear()
    matrix.fb.fill_rect(2,margin,current_width, height, 0xF800)
    matrix.fb.rect(2,margin,max_width, height, 0xF800)

    await matrix.show()

async def toast_display():
    matrix = NeoPixelMatrixAsync(23 ,32, 8)

    await matrix.scroll_text("Happy Toasting!", delay=0)
    await matrix.scroll_text("Heating.", delay=0.01)
    elapsed_time = 0
    while elapsed_time < 81:
        elapsed_time = time.ticks_diff(time.ticks_ms(), start_time) // 1000
        await draw_progress_bar(matrix=matrix, now=elapsed_time, max=80)
        await asyncio.sleep(
            random.randint(2,10)
            )
        await timer(
            matrix,
            random.randint(3,15)
            )
        await matrix.scroll_text("Heating")
        asyncio.sleep(1)

    # Now is HOT
    await matrix.text("HOT", center=True)
    await asyncio.sleep(2)
    while 1:
        await matrix.text("HOT", center=True)
        await asyncio.sleep(
            random.randint(2,10)
            )
        await timer(
            matrix,
            random.randint(3,15)
            )


asyncio.run(
    toast_display()
)