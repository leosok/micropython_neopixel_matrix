import time
import neopixel
import machine
from neopixel_matrix import NeoPixelMatrix
from neopixel_matrix import Color
from neopixel_matrix_async import NeoPixelMatrixAsync
from neopixel_matrix_mock import MockNeoPixelMatrix
from utils import format_ticks
import uasyncio as asyncio
import random


DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
WIDTH = 32
HEIGHT = 8
DIRECTION = NeoPixelMatrix.HORIZONTAL
SLEEP_TIME = 1000
BRIGHTNESS= 0.4



def test_neopixel_matrix():
    #from neopixel_matrix import NeoPixelMatrix

    # Configure the pin number, width, and height

    matrix = NeoPixelMatrix(DATA_PIN, WIDTH, HEIGHT, direction=DIRECTION)


    # # Fill the entire matrix with a single color
    # matrix.fill((255, 0, 0))  # Red
    # matrix.show()
    # machine.lightsleep(SLEEP_TIME)

    # # Clear the matrix
    # matrix.clear()

    # Clear the matrix
    import time
    matrix.clear()

    # Draw static text
    light_red = Color.light_color(Color.WHITE, 0.3)
    matrix.text("1 Hello", 0, 0, (255, 255, 255))
    time.sleep(2)

    matrix.text("HOT", 0, 0, Color.GREEN, center=True)
    time.sleep(2)

    # Draw and scroll a long text
    light_red = Color.light_color(Color.RED, 0.1)
    matrix.text("Hello, world...", 0, 0, light_red) 
    matrix.scroll(0)


    # Clear the matrix
    # matrix.clear()

def test_neopixel_matrix_mock(text, x, y, color):
    print("test_neopixel_matrix_mock")
    mock_matrix = MockNeoPixelMatrix(32, 8, direction=NeoPixelMatrix.HORIZONTAL)
    mock_matrix.text(text, x, y, color)
    mock_matrix.show()
    
    

def test_async():
    matrix = NeoPixelMatrixAsync(DATA_PIN, WIDTH, HEIGHT, direction=DIRECTION, brightness=BRIGHTNESS)
    start_time = time.ticks_ms()

    async def scroll():
       # matrix.text("Hello, Leo!", 0, 0, Color.RED)
        # while True:  
        #     await matrix.scroll(delay=0, scroll_out=True, scroll_in=True)

        for i in range(2):
            print("scroll started")
            await matrix.scroll_text(
                "123456789!",
                color=Color.RED, 
                delay=0, 
                scroll_in=True, 
                scroll_out=True
                )
        
        await matrix.scroll_text(
            "Hallo Leo!",
            color=Color.RED, 
            delay=0, 
            scroll_in=True, 
            scroll_out=False
            )


    async def real_scroll():
        await matrix.scroll_text("Toaster heating.", delay=0.00)
        await matrix.scroll_text("Happy Toasting!", delay=0)
        await asyncio.sleep(1)
        await matrix.text("HOT", center=True)
        await asyncio.sleep(2)
        while 1:
            await matrix.text("HOT", center=True)
            await asyncio.sleep(
                random.randint(2,10)
                )
            await timer(
                random.randint(3,15)
                )


    async def timer(sec=10):
        for _ in range(sec):
            elapsed_time = time.ticks_diff(time.ticks_ms(), start_time)
            formatted_time = format_ticks(elapsed_time)
            await matrix.text(formatted_time, center=True)
            await asyncio.sleep(1)
    
    async def run():
        await asyncio.gather(
            real_scroll(),
            #timer()
             )
    # Run the test_async function
    asyncio.run(run())

def test_mock_neopixel_matrix():
    async def run():
        matrix = MockNeoPixelMatrix(WIDTH, HEIGHT)

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





mr = machine.reset

if __name__ == '__main__': 

    # matrix = NeoPixelMatrixAsync(DATA_PIN, WIDTH, HEIGHT, direction=DIRECTION, brightness=BRIGHTNESS)
    # asyncio.run(
    #      matrix.scroll_text("Happy Toasting!", delay=0.07)
    # )

    test_mock_neopixel_matrix()
    #test_async()

    #test_neopixel_matrix()


    #test_neopixel_matrix_mock("Hello!", 0, 0, (255, 255, 255))  # White
