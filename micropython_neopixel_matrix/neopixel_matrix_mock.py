# Not ideal but the quickest fix I could come up with
try: from neopixel_matrix import NeoPixelMatrix, Color
except ImportError: from micropython_neopixel_matrix.neopixel_matrix import NeoPixelMatrix, Color

import uasyncio as asyncio

import sys

class MockNeoPixelMatrix(NeoPixelMatrix):
    """
    A subclass of the NeoPixelMatrix class, which simulates a NeoPixel matrix by printing
    the matrix content to the console.

    The class overrides the show() method to display the matrix in the console instead
    of updating the NeoPixel hardware. The matrix content is represented by '#' characters
    for colored pixels and '-' characters for background pixels.

    Example usage:

        mock_matrix = MockNeoPixelMatrix(32, 8)
        mock_matrix.text('Hello World', 0, 0, color=Color.RED)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(0, *args, **kwargs)

    def _print_matrix(self, clear_screen=True):
        if clear_screen:
            sys.stdout.write('\033[2J\033[H')  # Clear screen and move cursor to top-left corner
        for y in range(self.height):
            row = ''
            for x in range(self.width):
                r, g, b = self._rgb565_to_rgb888(self.fb.pixel(x, y))
                if (r, g, b) == self.bg_color:
                    row += '-'
                else:
                    row += '#'
            print(row)
        print()

    def show(self, clear_screen=True):
        self._update_np_from_fb()
        self._print_matrix(clear_screen=clear_screen)


# class MockNeoPixelMatrixAsync(MockNeoPixelMatrix):
#     """
#     A subclass of the NeoPixelMatrix class, which simulates a NeoPixel matrix by printing
#     the matrix content to the console.

#     The class overrides the show() method to display the matrix in the console instead
#     of updating the NeoPixel hardware. The matrix content is represented by '#' characters
#     for colored pixels and '-' characters for background pixels.

#     Example usage:

#         mock_matrix = MockNeoPixelMatrix(32, 8)
#         mock_matrix.text('Hello World', 0, 0, color=Color.RED)

#     """

#     def __init__(self, *args, **kwargs):
#         super().__init__(0, *args, **kwargs)

#     async def _print_matrix(self, clear_screen=True):
#         print("print")
#         await self._print_matrix(clear_screen=clear_screen)

#     async def scroll_text(self, string, x=0, y=0, color=(255,0,0), delay=0.07, scroll_in=True, scroll_out=True):
#         scroll_range = self._get_scroll_text_range(
#             string, x=x, y=y, color=color, scroll_in=scroll_in, scroll_out=scroll_out)
#         for _ in range(scroll_range):
#             self.fb.scroll(-1, 0)
#             await self.show()
#             await asyncio.sleep(delay)

#     async def show(self, clear_screen=False):
#         self._update_np_from_fb()
#         await self._print_matrix(clear_screen=clear_screen)