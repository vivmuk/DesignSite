#!/usr/bin/env python3
"""Assemble captured demo frames into 320x200 animated GIF thumbnails."""
from pathlib import Path

from PIL import Image

FRAMES = Path("/tmp/interactive-frames")
OUT = Path(__file__).resolve().parent.parent / "public" / "interactive" / "thumbs"
SIZE = (320, 200)

OUT.mkdir(parents=True, exist_ok=True)
count = 0
for demo_dir in sorted(p for p in FRAMES.iterdir() if p.is_dir()):
    frames = sorted(demo_dir.glob("f*.png"))
    if not frames:
        continue
    images = []
    for frame in frames:
        im = Image.open(frame).convert("RGB").resize(SIZE, Image.Resampling.LANCZOS)
        images.append(im.convert("P", palette=Image.Palette.ADAPTIVE, colors=64))
    target = OUT / f"{demo_dir.name}.gif"
    images[0].save(target, save_all=True, append_images=images[1:], duration=90, loop=0,
                   optimize=True, disposal=2)
    count += 1
print(f"wrote {count} GIFs to {OUT}")
