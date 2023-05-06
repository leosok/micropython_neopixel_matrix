# from neopixel_matrix_async import NeoPixelMatrixAsync
# import uasyncio as asyncio

# class MockNeoPixelMatrix(NeoPixelMatrixAsync):
#     def __init__(self, *args, **kwargs):
#         super().__init__(pin=0, *args, **kwargs)

#     def _print_matrix(self):
#         print("printing matrix"")
#         for y in range(self.height):
#             row = ''
#             for x in range(self.width):
#                 r, g, b = self._rgb565_to_rgb888(self.fb.pixel(x, y))
#                 if (r, g, b) == self.bg_color:
#                     row += '-'
#                 else:
#                     row += '#'
#             print(row)
#         print()

#     async def show(self):
#         print("showing")
#         asyncio.run(self._update_np_from_fb())
#         self._print_matrix()

#     async def scroll_text(self, *args, **kwargs):
#         await super().scroll_text(*args, **kwargs)
#         print("Scroll complete")

from neopixel_matrix_async import NeoPixelMatrixAsync
import uasyncio as asyncio

class MockNeoPixelMatrix(NeoPixelMatrixAsync):
    def __init__(self, *args, **kwargs):
        super().__init__(0, *args, **kwargs)

    def _print_matrix(self):
        print("printing matrix")
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
        print("showing")
        await self._update_np_from_fb()
        self._print_matrix()