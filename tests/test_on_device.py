import time
from micropython_neopixel_matrix.neopixel_matrix_mock import MockNeoPixelMatrix
from micropython_neopixel_matrix.neopixel_matrix import Color, NeoPixelMatrix
from micropython_neopixel_matrix.neopixel_matrix_async import NeoPixelMatrixAsync
import uasyncio as asyncio
import random

DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
WIDTH = 32
HEIGHT = 8
DIRECTION = NeoPixelMatrix.HORIZONTAL
SLEEP_TIME = 0
BRIGHTNESS= 0.4



def test_async():
    matrix = NeoPixelMatrixAsync(DATA_PIN, WIDTH, HEIGHT, direction=DIRECTION, brightness=BRIGHTNESS)

    async def scroll():
       # matrix.text("Hello, Leo!", 0, 0, Color.RED)
        # while True:  
        #     await matrix.scroll(delay=0, scroll_out=True, scroll_in=True)

       
        await matrix.scroll_text(
            "Hi:)",
            color=Color.RED, 
            delay=SLEEP_TIME, 
            scroll_in=True, 
            scroll_out=False
            )

        await asyncio.sleep(3)

        await matrix.scroll_text(
            "I scroll out.",
            color=Color.RED, 
            delay=SLEEP_TIME, 
            scroll_in=True, 
            scroll_out=True
            )
        await asyncio.sleep(2)



    asyncio.run(scroll())


def test_progress():
    async def run():
        matrix = NeoPixelMatrixAsync(23 ,32, 8)
        await matrix.draw_progress_bar(progress=40, max_progress=80)
        await asyncio.sleep(2)
        matrix1 = NeoPixelMatrix(23 ,32, 8)
        for i in range (1,100, 5):
            matrix1.draw_progress_bar(progress=i, max_progress=100, color=Color.GREEN)
            await asyncio.sleep(0.2)
        await asyncio.sleep(1)
        await matrix.clear()

    asyncio.run(run())



def test_neopixel_matrix():
    matrix = NeoPixelMatrix(DATA_PIN, WIDTH, HEIGHT)
    matrix.clear()
    time.sleep(2)
    matrix.text("HOT", center=True)
    time.sleep(2)

def test_mock_neopixel_matrix():
    print("test_neopixel_matrix_mock")
    mock_matrix = MockNeoPixelMatrix(32, 8, direction=NeoPixelMatrix.HORIZONTAL)
    mock_matrix.text("Hallo", 0, 0, Color.RED)
    mock_matrix.show()
    time.sleep(2)
    mock_matrix.scroll_text("Hello from Berlin")
    

def run_tests():
    test_neopixel_matrix()
    test_async()
    test_progress()
    test_mock_neopixel_matrix()