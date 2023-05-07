from neopixel_matrix_mock import MockNeoPixelMatrix, MockNeoPixelMatrixAsync
from neopixel_matrix import Color, NeoPixelMatrix
from neopixel_matrix_async import NeoPixelMatrixAsync
import uasyncio as asyncio
import random

DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
WIDTH = 32
HEIGHT = 8
DIRECTION = NeoPixelMatrix.HORIZONTAL
SLEEP_TIME = 0
BRIGHTNESS= 0.4

matrix = NeoPixelMatrix(DATA_PIN, WIDTH, HEIGHT, direction=DIRECTION, brightness=BRIGHTNESS)


def test_np_mock_async():
    async def run():
        matrix = MockNeoPixelMatrixAsync(WIDTH, HEIGHT)

        await matrix.text("Hallo Welt!", 0, 0, Color.WHITE)
        await asyncio.sleep(2)

        await matrix.scroll_text(
            "Hello, World!",
            color=Color.YELLOW,
            delay=0.07,
            scroll_in=True,
            scroll_out=True
        )
    
    asyncio.run(run())



def test_async():
    matrix = NeoPixelMatrixAsync(DATA_PIN, WIDTH, HEIGHT, direction=DIRECTION, brightness=BRIGHTNESS)

    async def scroll():
       # matrix.text("Hello, Leo!", 0, 0, Color.RED)
        # while True:  
        #     await matrix.scroll(delay=0, scroll_out=True, scroll_in=True)

       
        await matrix.scroll_text(
            "Hi from Berlin",
            color=Color.RED, 
            delay=SLEEP_TIME, 
            scroll_in=True, 
            scroll_out=False
            )

        await asyncio.sleep(2)

        await matrix.scroll_text(
            "I scroll out of sight.",
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
        await asyncio.sleep(1)
        matrix1 = NeoPixelMatrix(23 ,32, 8)
        matrix1.draw_progress_bar(progress=40, max_progress=80, color=Color.GREEN)
        await asyncio.sleep(1)
        await matrix.clear()

    asyncio.run(run())





def test_neopixel_matrix():
    matrix = NeoPixelMatrix(DATA_PIN, WIDTH, HEIGHT)
    matrix.text("HOT", center=True)

def test_neopixel_matrix_mock(text, x, y, color):
    print("test_neopixel_matrix_mock")
    mock_matrix = MockNeoPixelMatrix(32, 8, direction=NeoPixelMatrix.HORIZONTAL)
    mock_matrix.text(text, x, y, color)
    mock_matrix.show()
    

def run_tests():
    test_neopixel_matrix()
    test_async()
    test_progress()
    test_np_mock_async()