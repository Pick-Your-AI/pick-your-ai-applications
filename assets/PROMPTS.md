# Generated art provenance

## assets/icon.png
- Date: 2026-10-30
- Tool and model: Codex CLI 0.164.0 built-in image generation (session 01a18b6e-2428-7bd1-aad9-b7c8b83636c5); model id not reported by the tool
- Seed: not supported
- Reference images: none
- Prompt (verbatim):

```text
Use your image generation capability to create ONE image. Do not modify any other files.

Create one square 1024 x 1024 px (1:1 aspect ratio) image of a single repository glyph: an application directory grid with a source link.

GLYPH: A 3 by 3 grid of rounded application tiles drawn as simple geometric outlines of uniform stroke width. One tile is slightly raised above the others. A thin chain-link thread runs from the raised tile to a small blank document page sitting above the grid, suggesting a directory of apps backed by cited sources. The tiles are empty outlines with nothing drawn inside them. Keep the document page clear of the other tiles so no outlines overlap.
STYLE: strictly flat 2D vector look: solid-colour strokes with crisp hard edges, constant stroke width, no glow, no blur, no shadow, no gradients, no noise, no texture, no anti-aliasing halo. The glyph is centred, about 600 to 660 px on each side, and sits entirely inside the central 688 x 688 px square. The background is one perfectly uniform flat solid colour, exactly #042F2E in every pixel from corner to corner: no vignette, no lighting falloff, no dithering, no grain, no gradient, nothing else on it.
PALETTE: all outlines in solid #0F766E (teal; a lighter teal #14B8A6 may be used only for the chain link). Exactly one small four-point accent spark, filled solid #FBBF24 (amber), at the top right corner of the raised tile; the spark is the only filled shape and the only #FBBF24 element.

No text, letters, numbers, words, logos or brand marks anywhere in the image. No human figures, no third-party IP, no app icons or recognisable product marks, no UI chrome, no watermark, no border or frame, no extra sparks.

RENDERING: produce this as a flat vector-style graphic, as if exported from a vector editor onto a single filled rectangle of #042F2E. Every one of the four corners and every edge pixel of the canvas must be identical #042F2E; do not darken or lighten any region of the background, including the bottom-left corner.
```

- Candidates: 1 per attempt, 3 attempts (1 and 2 rejected: icon-ground, corner spread over the 3.0 limit); selected: attempt 3 (flat teal strokes, one amber spark, uniform ground)
- Post-processing: showcase.py 1.0.0 `content icon normalize --option A --ground transparent`; output sha256 59220200a0557fb096aec062ad6ab9fb904b0675f999ea2c3bc78b1eb47eaa24; size 109.6 KB
