# -*- coding: utf-8 -*-
# NeoPixel Matrix for MicroPython
# Used with ESP32 and 8x32 WS2812b LED matrix
# neopixel_matrix.py

from neopixel_matrix import NeoPixelMatrix, Color
import uasyncio as asyncio
import framebuf


class NeoPixelMatrixAsync(NeoPixelMatrix):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _update_np_from_fb(self):
        # Calling the synchronous _update_np_from_fb method from the superclass
        super()._update_np_from_fb()
        await asyncio.sleep_ms(0)  # Yield to other tasks

    async def show(self):
        await self._update_np_from_fb()
        self.np.write()

    async def text(self, string, x=0, y=0, color=Color.RED, center=False):
        super().text(string, x, y, color, center)
        await self.show()

    async def scroll_text(self, string, x=0, y=0, color=Color.RED, delay=0.07, scroll_in=True, scroll_out=True):
        scroll_range = self._get_scroll_text_range(
            string, x=x, y=y, color=color, scroll_in=scroll_in, scroll_out=scroll_out)
        for _ in range(scroll_range):
            self.fb.scroll(-1, 0)
            for _ in range(scroll_range):
                await self.show()
                await asyncio.sleep(delay)
