from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math


# ==========================================================
# CONSTANTS
# ==========================================================
#
# CELL:
#   Size (in output PDF pixels) used to display one mosaic
#   pixel/sticker. A larger value makes the instruction
#   diagrams easier to read.
#
# CHUNK_SIZE:
#   Maximum number of mosaic pixels processed per page.
#
#   Since one Rubik's Cube face is 3×3 stickers:
#
#       3 cubes × 3 stickers = 9 pixels
#
#   Therefore:
#
#       CHUNK_SIZE = 9
#
#   means one instruction page can contain at most a
#   3×3 arrangement of Rubik's cubes.
#
# PAGE_SIZE:
#   Size of the instruction pages generated.
#
# ==========================================================

CELL = 40
CHUNK_SIZE = 9
PAGE_SIZE = 900


# ==========================================================
# rgb_to_hex
# ==========================================================
#
# Converts an RGB tuple into hexadecimal notation.
#
# Example:
#
#     (255, 0, 0)
#
# becomes:
#
#     "#ff0000"
#
# This function is not currently used in the PDF generation
# pipeline, but it can be useful later if colors need to be
# exported to HTML, JSON, text instructions, etc.
#
# ==========================================================

def rgb_to_hex(rgb):

    return '#%02x%02x%02x' % tuple(rgb)

# ==========================================================
# create_overview_page
# ==========================================================
#
# Creates the FIRST page of the PDF.
#
# This page serves as a map of the entire mosaic and shows
# how the mosaic has been divided into printable chunks.
#
# Example:
#
# Suppose the mosaic dimensions are:
#
#       23 × 17 pixels
#
# Since each instruction page can contain at most:
#
#       9 × 9 pixels
#
# the mosaic is divided into:
#
#       ceil(23/9) = 3 chunks horizontally
#       ceil(17/9) = 2 chunks vertically
#
# producing:
#
#       A1  B1  C1
#       A2  B2  C2
#
# The final chunks may be smaller than 9×9 if the image
# dimensions are not exact multiples of 9.
#
# This overview page visually communicates those divisions.
#
# ==========================================================

def create_overview_page(image):

    #
    # Create a blank page with a light gray background.
    #
    page = Image.new(
        'RGB',
        (1200, 1200),
        (240, 240, 240)
    )

    draw = ImageDraw.Draw(page)

    #
    # Create a large preview of the complete mosaic.
    #
    # NEAREST interpolation preserves the blocky appearance
    # of the mosaic instead of blurring the colors.
    #
    OVERVIEW_SCALE = 10

    preview_w = image.width * OVERVIEW_SCALE
    preview_h = image.height * OVERVIEW_SCALE

    preview = image.resize(
        (preview_w, preview_h),
        Image.Resampling.NEAREST
    )

    offset_x = 50
    offset_y = 50

    page.paste(
        preview,
        (offset_x, offset_y)
    )

    #
    # Determine how many instruction chunks are needed.
    #
    # ceil() is used because the last chunk may contain
    # fewer than 9 pixels.
    #
    # Example:
    #
    #     width = 23 pixels
    #
    # gives:
    #
    #     ceil(23/9) = 3 chunks
    #
    cols = math.ceil(image.width / CHUNK_SIZE)
    rows = math.ceil(image.height / CHUNK_SIZE)

    #
    # Size of one chunk box on the overview image.
    #
    cell_w = preview_w / cols
    cell_h = preview_h / rows
    #
    # Labels used for chunk identification.
    #
    # Columns:
    #
    #     A, B, C, ...
    #
    # Rows:
    #
    #     1, 2, 3, ...
    #
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    font = ImageFont.truetype(
        'arial.ttf',
        25
    )

    #
    # Draw chunk boundaries and labels.
    #
    for row in range(rows):

        for col in range(cols):

            #
            # Determine actual chunk dimensions.
            #
            # Most chunks are 9×9 pixels.
            #
            # Edge chunks may be smaller.
            #
            actual_w = min(
                CHUNK_SIZE,
                image.width - col * CHUNK_SIZE
            )

            actual_h = min(
                CHUNK_SIZE,
                image.height - row * CHUNK_SIZE
            )

            #
            # Position of this chunk on the overview page.
            #
            x = offset_x + col * cell_w
            y = offset_y + row * cell_h

            #
            # Scale edge chunks proportionally.
            #
            # Example:
            #
            # If only 5 pixels remain horizontally,
            # the box occupies 5/9 of the normal width.
            #
            x2 = x + cell_w * actual_w / CHUNK_SIZE
            y2 = y + cell_h * actual_h / CHUNK_SIZE

            #
            # Draw chunk boundary.
            #
            draw.rectangle(
                [x, y, x2, y2],
                outline='black',
                width=3
            )

            #
            # Generate chunk label.
            #
            # Examples:
            #
            #     col=0,row=0 → A1
            #     col=1,row=0 → B1
            #     col=0,row=1 → A2
            #
            label = f'{letters[col]}{row+1}'

            #
            # Draw label inside the chunk.
            #
            draw.text(
                (x + 10, y + 10),
                label,
                fill='black',
                font=font
            )

    #
    # Return the completed overview page.
    #
    return page


# ==========================================================
# create_page
# ==========================================================
#
# Generates one instruction page corresponding to a single
# chunk of the mosaic.
#
# Layout of the page:
#
# ┌───────────────────────────────────────────────┐
# │ Chunk Preview     Label          Mini Map     │
# │                                               │
# │                                               │
# │                                               │
# │      Enlarged Chunk Instructions              │
# │                                               │
# │  Thick lines every 3 stickers indicate        │
# │  Rubik's Cube boundaries.                     │
# └───────────────────────────────────────────────┘
#
# Inputs:
#
# chunk:
#     Cropped portion of the mosaic.
#
# label:
#     Chunk identifier (A1, B2, C3, ...)
#
# full_image:
#     Entire mosaic image.
#
# row, col:
#     Chunk location within the mosaic.
#
# ==========================================================

def create_page(chunk, label, full_image, row, col):

    #
    # Create blank instruction page.
    #
    page = Image.new(
        'RGB',
        (900, 900),
        (240, 240, 240)
    )

    draw = ImageDraw.Draw(page)

    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # ======================================================
    # Mini overview map
    # ======================================================
    #
    # This shows the complete mosaic in the corner.
    # The current chunk is highlighted in red so the
    # builder knows where they are.
    #
    MINIMAP_SCALE = 5

    overview_w = full_image.width * MINIMAP_SCALE
    overview_h = full_image.height * MINIMAP_SCALE

    overview = full_image.resize(
        (overview_w, overview_h),
        Image.Resampling.NEAREST
    )

    overview_x = 620
    overview_y = 20

    page.paste(
        overview,
        (overview_x, overview_y)
    )

    #
    # Number of chunks in the mosaic.
    #
    cols = math.ceil(full_image.width / CHUNK_SIZE)
    rows = math.ceil(full_image.height / CHUNK_SIZE)

    cell_w = overview_w / cols
    cell_h = overview_h / rows

    font_small = ImageFont.truetype(
        'arial.ttf',
        18
    )

    #
    # Draw chunk boundaries on the mini map.
    #
    for r in range(rows):

        for c in range(cols):

            #
            # Edge chunks may be smaller.
            #
            actual_w = min(
                CHUNK_SIZE,
                full_image.width - c * CHUNK_SIZE
            )

            actual_h = min(
                CHUNK_SIZE,
                full_image.height - r * CHUNK_SIZE
            )

            x = overview_x + c * cell_w
            y = overview_y + r * cell_h

            x2 = x + cell_w * actual_w / CHUNK_SIZE
            y2 = y + cell_h * actual_h / CHUNK_SIZE

            #
            # Highlight current chunk.
            #
            if r == row and c == col:
                outline = 'red'
                width = 5
            else:
                outline = 'black'
                width = 2

            draw.rectangle(
                [x, y, x2, y2],
                outline=outline,
                width=width
            )

            #
            # Draw chunk label.
            #
            label_text = f'{letters[c]}{r+1}'

            draw.text(
                (x + 5, y + 5),
                label_text,
                fill='black',
                font=font_small
            )

    # ======================================================
    # Chunk preview
    # ======================================================
    #
    # Shows the actual chunk at a glance.
    #
    PREVIEW_SCALE = 20

    preview = chunk.resize(
        (
            chunk.width * PREVIEW_SCALE,
            chunk.height * PREVIEW_SCALE
        ),
        Image.Resampling.NEAREST
    )

    page.paste(preview, (20, 20))

    # ======================================================
    # Large chunk label
    # ======================================================
    #
    # Makes it easy to identify pages after printing.
    #
    font_large = ImageFont.truetype(
        'arial.ttf',
        180
    )

    draw.text(
        (250, 0),
        label,
        fill='black',
        font=font_large
    )

    # ======================================================
    # Enlarged instruction diagram
    # ======================================================
    #
    # Each mosaic pixel becomes a large square.
    #
    start_x = 20
    start_y = 220

    pixels = chunk.load()

    chunk_w = chunk.width
    chunk_h = chunk.height

    # ======================================================
    # Draw individual stickers
    # ======================================================
    #
    # Every mosaic pixel becomes one enlarged sticker.
    #
    for py in range(chunk_h):

        for px in range(chunk_w):

            color = tuple(
                pixels[px, py]
            )

            #
            # Convert mosaic coordinates into
            # page coordinates.
            #
            x1 = start_x + px * CELL
            y1 = start_y + py * CELL

            x2 = x1 + CELL
            y2 = y1 + CELL

            #
            # Draw sticker.
            #
            draw.rectangle(
                [x1, y1, x2, y2],
                fill=color,
                outline='gray',
                width=1
            )

    # ======================================================
    # Draw Rubik's Cube boundaries
    # ======================================================
    #
    # Every 3 stickers correspond to one cube face.
    #
    # Sticker grid:
    #
    #     □ □ □ | □ □ □ | □ □ □
    #     □ □ □ | □ □ □ | □ □ □
    #     □ □ □ | □ □ □ | □ □ □
    #     -------+-------+------
    #
    # Thick lines visually separate cubes.
    #
    for py in range(0, chunk_h + 1, 3):

        y = start_y + py * CELL

        draw.line(
            [
                (start_x, y),
                (start_x + chunk_w * CELL, y)
            ],
            fill='black',
            width=5
        )

    for px in range(0, chunk_w + 1, 3):

        x = start_x + px * CELL

        draw.line(
            [
                (x, start_y),
                (x, start_y + chunk_h * CELL)
            ],
            fill='black',
            width=5
        )

    # ======================================================
    # Outer border
    # ======================================================
    #
    # Gives the entire instruction area a clear edge.
    #
    draw.rectangle(
        [
            start_x,
            start_y,
            start_x + chunk_w * CELL,
            start_y + chunk_h * CELL
        ],
        outline='black',
        width=6
    )

    #
    # Return completed page.
    #
    return page


# ==========================================================
# export_pdf
# ==========================================================
#
# Main PDF generation function.
#
# Workflow:
#
#     Input Mosaic
#           │
#           ▼
#   Create Overview Page
#           │
#           ▼
#   Divide Mosaic Into Chunks
#           │
#           ▼
#   Generate One Page Per Chunk
#           │
#           ▼
#      Return All Pages
#
#
# Example:
#
# Suppose the mosaic size is:
#
#       width  = 23 pixels
#       height = 17 pixels
#
# Since each instruction chunk can contain:
#
#       9 × 9 pixels maximum
#
# we need:
#
#       ceil(23 / 9) = 3 chunks horizontally
#       ceil(17 / 9) = 2 chunks vertically
#
# giving:
#
#       A1  B1  C1
#       A2  B2  C2
#
# The last chunks automatically become smaller:
#
#       C1 → 5 × 9
#       A2 → 9 × 8
#       B2 → 9 × 8
#       C2 → 5 × 8
#
# ==========================================================

def export_pdf(image):

    #
    # Determine how many chunks are required.
    #
    # ceil() is important here.
    #
    # Example:
    #
    #     width = 23
    #
    #     23 / 9 = 2.55...
    #
    # We still need the third chunk to store the
    # remaining 5 pixels.
    #
    chunk_cols = math.ceil(
        image.width / CHUNK_SIZE
    )

    chunk_rows = math.ceil(
        image.height / CHUNK_SIZE
    )

    #
    # List that will store all generated pages.
    #
    # The final PDF will simply be these pages
    # stitched together in order.
    #
    pages = []

    # ======================================================
    # Generate overview page
    # ======================================================
    #
    # This becomes Page 1 of the PDF.
    #
    overview_page = create_overview_page(
        image
    )

    pages.append(
        overview_page
    )

    #
    # Column labels.
    #
    # Examples:
    #
    #     col = 0 → A
    #     col = 1 → B
    #     col = 2 → C
    #
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    # ======================================================
    # Generate chunk instruction pages
    # ======================================================
    #
    # Chunks are processed row by row.
    #
    # Example:
    #
    #       A1 → B1 → C1
    #       A2 → B2 → C2
    #
    # This ordering makes assembly easier.
    #
    for row in range(chunk_rows):

        for col in range(chunk_cols):

            #
            # Compute top-left corner of chunk
            # in mosaic coordinates.
            #
            x1 = col * CHUNK_SIZE
            y1 = row * CHUNK_SIZE

            #
            # Compute bottom-right corner.
            #
            # Edge chunks may extend beyond the
            # mosaic dimensions, so min() keeps
            # them inside the image.
            #
            x2 = min(
                x1 + CHUNK_SIZE,
                image.width
            )

            y2 = min(
                y1 + CHUNK_SIZE,
                image.height
            )

            #
            # Extract chunk from the mosaic.
            #
            # Examples:
            #
            # Normal chunk:
            #
            #     (0,0) → (9,9)
            #
            # Edge chunk:
            #
            #     (18,0) → (23,9)
            #
            # producing a 5×9 chunk.
            #
            chunk = image.crop(
                (
                    x1,
                    y1,
                    x2,
                    y2
                )
            )

            #
            # Generate chunk label.
            #
            # Examples:
            #
            #     row=0,col=0 → A1
            #     row=0,col=1 → B1
            #     row=1,col=0 → A2
            #
            label = (
                f'{letters[col]}{row + 1}'
            )

            #
            # Generate instruction page for
            # this chunk.
            #
            page = create_page(
                chunk=chunk,
                label=label,
                full_image=image,
                row=row,
                col=col
            )

            #
            # Add page to PDF sequence.
            #
            pages.append(page)

    #
    # Return all pages.
    #
    # The caller can save them directly as a PDF.
    #
    return pages

