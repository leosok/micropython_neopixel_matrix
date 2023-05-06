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
           

    # async def scroll(self, delay=0.1, scroll_out=True):
    #     fb_width = self.fb_width
    #     if scroll_out:
    #         scroll_range =  fb_width + self.width
    #     else:
    #         scroll_range = fb_width - self.width + 1
    #     for i in range(scroll_range):
    #         self.fb.scroll(-1, 0)
    #         await self.show()
    #         await asyncio.sleep(delay)

    async def scroll(self, delay=0.1, scroll_range=None):
        fb_width = self.fb_width
        if scroll_range is None:
            start, end = 0, fb_width - self.width + 1
        else:
            start, end = scroll_range

        for i in range(start, end):
            self.fb.scroll(-1, 0)
            await self.show()
            await asyncio.sleep(delay)

    # async def scroll_text(self, string, x=0, y=0, color=Color.RED, delay=0, scroll_in=True, scroll_out=True):
    #     text_width = self._get_text_width(string)

    #     if scroll_in:
    #         initial_x = self.width
    #     else:
    #         initial_x = x

    #     if scroll_out:
    #         fb_width = text_width + self.width
    #     else:
    #         fb_width = max(text_width, self.width)

    #     self._update_framebuffer_size(fb_width)
    #     self.fill(self.bg_color)
    #     self._draw_text_to_buffer(string, initial_x, y, color, self.fb)

    #     if scroll_in:
    #         start_scroll = 0
    #         end_scroll = self.width + text_width
    #     else:
    #         start_scroll = initial_x
    #         end_scroll = text_width - initial_x

    #     for i in range(start_scroll, end_scroll):
    #         self.fb.scroll(-1, 0)
    #         await self.show()
    #         await asyncio.sleep(delay)

    
    async def scroll_text(self, string, x=0, y=0, color=Color.RED, delay=0.07, scroll_in=True, scroll_out=True):
        text_width = self._get_text_width(string)
        
        if scroll_in:
            fb_width = text_width + self.width # all text outside the FB
            x = fb_width - text_width # start at the right edge
        else:
            fb_width = max(text_width, self.width)
            
        self._update_framebuffer_size(fb_width)
        
        self.fill(self.bg_color)
        self._draw_text_to_buffer(string, x, y, color, self.fb)

        scroll_range = fb_width - self.width # will stop at the left of the matrix
        if scroll_out:
            scroll_range += self.width # will go on to get out to the left

        for _ in range(scroll_range):
            self.fb.scroll(-1, 0)
            await self.show()
            await asyncio.sleep(delay)

