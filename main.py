#!/usr/bin/env python3
"""Entry program for make.fun bounty the-poster-for-a-place-that-i-2-20261121-0539.

Run with: python3 main.py
Builds the Velmara poster via the generate_image module and writes it to
/output/entry.png. Pillow only, no network, fully deterministic (the
drawing code uses a fixed-seed PRNG, so repeated runs are byte-identical).
"""

import os

import generate_image

OUTPUT_PATH = "/output/entry.png"


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    generate_image.main(OUTPUT_PATH)


if __name__ == "__main__":
    main()
