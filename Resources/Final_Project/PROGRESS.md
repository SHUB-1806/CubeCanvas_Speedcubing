# CubeCanvas: day-by-day progression

Each folder is a complete runnable snapshot. Every new day keeps the working features from the previous day and adds only the feature listed below.

## Setup

From the `CubeCanvas` folder, install the shared dependencies once:

```powershell
python -m pip install -r requirements.txt
```

Then enter any day folder and run:

```powershell
python main.py
```

## Feature sequence

1. **Day 1 — Select an image:** open the file picker and print the selected path.
2. **Day 2 — Display the image:** introduce stacked pages and show the selected image on Page 2.
3. **Day 3 — Responsive fitting:** preserve the aspect ratio and refit the image whenever the window changes size.
4. **Day 4 — Reusable fitting and Page 2 layout:** move fitting into `fit_image_to_frame()` and divide Page 2 into a toolbar, controls, and image panel.
5. **Day 5 — Complete Page 2 controls:** add cube rows/columns, total cube count, editable palette, and close/back navigation.
6. **Day 6 — Crosshair:** change the image display to a canvas and add bounded crosshair guides. The Day 3 responsive fitting remains active.
7. **Day 7 — Crop rectangle:** add click-and-drag crop selection constrained to the mosaic's `columns / rows` aspect ratio. Responsive fitting remains active.
8. **Day 8 — Mosaic preview:** confirm the crop, quantize it to the six-color palette, and add Page 3 with synchronized original/mosaic previews.
9. **Day 9 — Image effects:** add brightness, contrast, saturation, sharpness, blur, flips, mosaic blur, and revert controls.
10. **Day 10 — PDF export:** export an overview and numbered build-instruction pages to a PDF selected by the user.

## Reusable code introduced progressively

- `show_page()` handles navigation instead of duplicating page-switching code.
- `fit_image_to_frame()` is introduced on Day 4 and reused on every later Page 2.
- `p1_`, `p2_`, and `p3_` widget-builder functions keep layout code separate from application behavior.
- `update_color_box()` serves every editable palette row.
- `fit_image_canvas()` serves both Page 3 preview canvases.
- `apply_effects()` composes the individual image-processing helpers without repeatedly modifying the source image.
- `export_pdf()` delegates overview and instruction-page construction to focused helper functions.

## Corrections made during the continuity audit

- Restored the missing resize binding in Days 6 and 7.
- Corrected crop aspect ratio from `rows / columns` to `columns / rows` in Days 7–10.
- Invalidated stale crop coordinates after a resize so the wrong source area cannot be confirmed.
- Corrected the visible “Columns” spelling in Days 5–10.
- Removed generated cache files and the accidental `tempCodeRunnerFile.py` file.
- Removed a Day 10 debug print that referred to the global `app` instead of the current instance.
- Corrected the Day 4 folder-name spelling.
