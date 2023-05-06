

from neopixel_matrix_async import NeoPixelMatrixAsync
import uasyncio as asyncio

class MockNeoPixelMatrix(NeoPixelMatrixAsync):
    def __init__(self, *args, **kwargs):
        super().__init__(0, *args, **kwargs)


    def _move_cursor_up(self, lines):
        print("\033[{}A".format(lines), end="")

    def _clear_line(self):
        print("\033[K", end="")

    def _print_matrix(self):
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

    async def show(self):
        await self._update_np_from_fb()
        self._print_matrix()



if __name__ == '__main__':
    mock_matrix = MockNeoPixelMatrix(32, 8)
    mock_matrix.text('Hello World', 0, 0, color=mock_matrix.Color.RED)