from setuptools import setup

setup(
    name="micropython_neopixel_matrix",
    version="0.1",
    description="NeoPixel Matrix library for MicroPython. Used with WS2812b Matrix.",
    author="Leonid Sokolov",
    author_email="leosok@gmx.de",
    url="https://github.com/yourusername/micropython_neopixel_matrix",
    packages=["micropython_neopixel_matrix"],
    install_requires=["micropython", "micropython-uasyncio"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: Implementation :: MicroPython",
        "Topic :: Software Development :: Libraries",
    ],
)