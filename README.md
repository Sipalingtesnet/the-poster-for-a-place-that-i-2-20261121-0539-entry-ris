# The Poster for a Place That Isn't There — Velmara

Velmara is a place that does not exist: floating terraced islands drifting above an amber sea at sunset, their sunlit olive tops stepped like ancient rice terraces, waterfalls spilling off the rocky keels into the glowing water below. A giant low sun bands the teal-to-amber sky, birds cross the dusk, dark framing cliffs anchor the corners, and a white lighthouse with a warm vintage band stands on the highest terrace of the main island, its beam sweeping the horizon. The only text is the place name, VELMARA, in cream serif letters — a vintage travel poster for a destination you can only imagine.

## How the entry works

Running `python3 main.py` imports the `generate_image` module and calls its image-building function with the output path `/output/entry.png` (the directory is created if needed). The entire poster is drawn from scratch with Pillow primitives — gradients, polygons, ellipses, arcs and a bundled system serif font. There is no network access, no external images, and no randomness beyond a fixed-seed PRNG, so the output is fully deterministic: repeated runs produce byte-identical files. Running `python3 generate_image.py` directly still writes `entry.png` in the repo root.

## Gate facts

- Output: valid PNG, exactly 1024x1024 pixels
- File size: under 1 MiB
- Deterministic: two runs yield identical sha256 checksums
- Dependencies: Pillow only

## Badges

[![Bounty](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Sipalingtesnet/the-poster-for-a-place-that-i-2-20261121-0539-entry-ris/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/Sipalingtesnet/the-poster-for-a-place-that-i-2-20261121-0539-entry-ris/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
