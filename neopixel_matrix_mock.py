from neopixel_matrix import NeoPixelMatrix 
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

    def _print_matrix(self):
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

    def show(self):
        self._update_np_from_fb()
        self._print_matrix()
        

class MockNeoPixelMatrixAsync(NeoPixelMatrix):
    def __init__(self, *args, **kwargs):
        super().__init__(0, *args, **kwargs)

    async def _print_matrix(self):
        await super().__init__(0, *args, **kwargs)

    async def show(self):
        await self._update_np_from_fb()
        await self._print_matrix()