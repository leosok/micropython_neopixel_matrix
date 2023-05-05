import neopixel
import machine
from neopixels_matrix import NeoPixelMatrix, MockNeoPixelMatrix
from neopixels_matrix import Color


def test_neopixel_matrix():
    #from neopixel_matrix import NeoPixelMatrix

    # Configure the pin number, width, and height
    DATA_PIN = 23  # GPIO5 on ESP8266, change this to the pin you have connected to the Neopixels
    WIDTH = 32
    HEIGHT = 8
    DIRECTION = NeoPixelMatrix.HORIZONTAL
    SLEEP_TIME = 1000


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
    matrix.text("1 Hello", 0, 0, (255, 255, 255))
    time.sleep(1)


    # Draw and scroll a long text
    light_red = Color.light_color(Color.RED, 0.1)
    matrix.text("Hello, world...", 0, 0, light_red) 
    matrix.scroll(0.02)


    # Clear the matrix
    # matrix.clear()

def test_neopixel_matrix_mock(text, x, y, color):
    print("test_neopixel_matrix_mock")
    mock_matrix = MockNeoPixelMatrix(32, 8, direction=NeoPixelMatrix.HORIZONTAL)
    mock_matrix.text(text, x, y, color)
    mock_matrix.show()
    
    



if __name__ == '__main__': 
    test_neopixel_matrix()


    #test_neopixel_matrix_mock("Hello!", 0, 0, (255, 255, 255))  # White