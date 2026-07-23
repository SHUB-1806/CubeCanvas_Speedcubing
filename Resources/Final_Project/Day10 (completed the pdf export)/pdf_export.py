from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math


# ==========================================================
# PDF EXPORT SETTINGS
# ==========================================================

PAGE_SIZE = (1200, 1200)
PAGE_BG = (245, 247, 250)
INK = (25, 28, 33)
MUTED = (91, 101, 114)
PANEL = (255, 255, 255)
PANEL_BORDER = (190, 198, 210)
ACCENT = (220, 38, 38)
GRID_LINE = (122, 130, 142)
CUBE_LINE = (18, 24, 32)
CHUNK_SIZE = 9
STICKERS_PER_CUBE = 3


def rgb_to_hex(rgb):
    # Keep color names export-ready for any future HTML, CSV, or legend output.
    return '#%02x%02x%02x' % tuple(rgb[:3])


def load_font(size, bold=False):
    # Try common Windows fonts first because this project is a desktop Tk app.
    font_names = (
        ("arialbd.ttf", "Arial Bold.ttf") if bold else ("arial.ttf", "Arial.ttf")
    )

    for font_name in font_names:
        try:
            return ImageFont.truetype(font_name, size)
        except OSError:
            pass

    # Pillow's built-in font keeps PDF export working on machines without Arial.
    return ImageFont.load_default()


def chunk_label(col, row):
    # Convert 0-based columns into spreadsheet-style labels: A...Z, AA...AZ.
    label = ""
    col_number = col + 1

    while col_number:
        col_number, remainder = divmod(col_number - 1, 26)
        label = chr(65 + remainder) + label

    return f"{label}{row + 1}"


def text_size(draw, text, font):
    # textbbox gives exact dimensions and avoids deprecated textsize behavior.
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def fit_font_to_box(draw, text, start_size, max_w, max_h, bold=False, min_size=8):
    # Shrink bounded text until it fits the available outline area.
    for size in range(start_size, min_size - 1, -1):
        font = load_font(size, bold=bold)
        text_w, text_h = text_size(draw, text, font)

        if text_w <= max_w and text_h <= max_h:
            return font

    # Returning None lets callers skip text that cannot be made readable safely.
    return None


def draw_text_fit(draw, box, text, size, fill=INK, bold=False, anchor="left", min_size=8):
    # Draw one line only when it can be kept inside its assigned rectangle.
    max_w = box[2] - box[0]
    max_h = box[3] - box[1]
    font = fit_font_to_box(draw, text, size, max_w, max_h, bold=bold, min_size=min_size)

    if font is None:
        return False

    text_w, text_h = text_size(draw, text, font)
    x = box[0] if anchor == "left" else box[0] + (max_w - text_w) / 2
    y = box[1] + (max_h - text_h) / 2
    draw.text((x, y), text, fill=fill, font=font)
    return True


def draw_panel(draw, box, title=None):
    # A light panel groups each PDF feature without hiding the mosaic content.
    draw.rounded_rectangle(box, radius=18, fill=PANEL, outline=PANEL_BORDER, width=2)

    if title:
        draw_text_fit(
            draw,
            (box[0] + 22, box[1] + 12, box[2] - 22, box[1] + 48),
            title,
            24,
            bold=True,
        )


def fit_size(source_w, source_h, max_w, max_h, allow_upscale=True):
    # Use one scale for both axes so every non-square mosaic keeps its aspect ratio.
    if source_w <= 0 or source_h <= 0 or max_w <= 0 or max_h <= 0:
        return 1, 1

    scale = min(max_w / source_w, max_h / source_h)

    if not allow_upscale:
        scale = min(scale, 1)

    return max(1, int(source_w * scale)), max(1, int(source_h * scale))


def paste_fit(page, image, box, border=True):
    # Resize a preview into the provided box instead of relying on fixed scales.
    max_w = box[2] - box[0]
    max_h = box[3] - box[1]
    fitted_w, fitted_h = fit_size(image.width, image.height, max_w, max_h)
    preview = image.resize((fitted_w, fitted_h), Image.Resampling.NEAREST)
    x = box[0] + (max_w - fitted_w) // 2
    y = box[1] + (max_h - fitted_h) // 2

    page.paste(preview, (x, y))

    if border:
        ImageDraw.Draw(page).rectangle(
            [x, y, x + fitted_w, y + fitted_h],
            outline=PANEL_BORDER,
            width=2,
        )

    return (x, y, fitted_w, fitted_h)


def chunk_counts(image):
    # Ceiling division includes partial right/bottom edge chunks in the plan.
    return math.ceil(image.width / CHUNK_SIZE), math.ceil(image.height / CHUNK_SIZE)


def chunk_bounds(image, col, row):
    # Clamp every crop to the mosaic bounds so edge chunks can be smaller safely.
    x1 = col * CHUNK_SIZE
    y1 = row * CHUNK_SIZE
    x2 = min(x1 + CHUNK_SIZE, image.width)
    y2 = min(y1 + CHUNK_SIZE, image.height)
    return x1, y1, x2, y2


def draw_chunk_grid(draw, image, placed_box, current=None, show_labels=True):
    # Draw chunk lines using pixel scale, not row/column averages; this fixes
    # rectangular mosaics and final chunks that are narrower or shorter than 9.
    x, y, displayed_w, displayed_h = placed_box
    scale_x = displayed_w / image.width
    scale_y = displayed_h / image.height
    cols, rows = chunk_counts(image)
    label_font = load_font(16, bold=True)

    for row in range(rows):
        for col in range(cols):
            x1, y1, x2, y2 = chunk_bounds(image, col, row)
            box = [
                x + x1 * scale_x,
                y + y1 * scale_y,
                x + x2 * scale_x,
                y + y2 * scale_y,
            ]

            is_current = current == (row, col)
            outline = ACCENT if is_current else CUBE_LINE
            width = 5 if is_current else 2
            draw.rectangle(box, outline=outline, width=width)

            if show_labels:
                label = chunk_label(col, row)
                label_box = [box[0] + 5, box[1] + 5, box[2] - 5, box[3] - 5]
                label_font = fit_font_to_box(
                    draw,
                    label,
                    16,
                    label_box[2] - label_box[0] - 10,
                    label_box[3] - label_box[1] - 8,
                    bold=True,
                    min_size=7,
                )

                if label_font:
                    text_w, text_h = text_size(draw, label, label_font)
                    tag = [
                        label_box[0],
                        label_box[1],
                        min(label_box[0] + text_w + 10, label_box[2]),
                        min(label_box[1] + text_h + 8, label_box[3]),
                    ]
                    draw.rounded_rectangle(tag, radius=5, fill=(255, 255, 255), outline=outline, width=1)
                    draw_text_fit(draw, (tag[0] + 5, tag[1] + 2, tag[2] - 5, tag[3] - 2), label, 16, bold=True, min_size=7)


def draw_color_palette(draw, image, box):
    # Show the actual exported color set so the builder can audit available stickers.
    colors = image.convert("RGB").getcolors(maxcolors=image.width * image.height)
    colors = sorted(colors or [], key=lambda item: item[0], reverse=True)
    total = max(1, image.width * image.height)
    heading = load_font(22, bold=True)
    font = load_font(17)
    swatch = 28
    gap = 10
    x = box[0]
    y = box[1]

    draw.text((x, y), "Color key", fill=INK, font=heading)
    y += 38

    for index, (count, color) in enumerate(colors[:12], start=1):
        if y + swatch > box[3]:
            break

        draw.rectangle([x, y, x + swatch, y + swatch], fill=color, outline=CUBE_LINE, width=1)
        label = f"{index}. {rgb_to_hex(color)}  {count} stickers  ({count / total:.0%})"
        draw_text_fit(draw, (x + swatch + gap, y, box[2], y + swatch), label, 17, fill=INK)
        y += swatch + 11

    if len(colors) > 12:
        draw_text_fit(draw, (x, y, box[2], y + 28), f"+ {len(colors) - 12} more colors", 17, fill=MUTED)


def create_overview_page(image):
    # Build the PDF cover page as an explicit guide, not just a raw picture dump.
    page = Image.new("RGB", PAGE_SIZE, PAGE_BG)
    draw = ImageDraw.Draw(page)
    title_font = load_font(46, bold=True)
    subtitle_font = load_font(22)
    stat_font = load_font(20, bold=True)
    cols, rows = chunk_counts(image)
    cube_cols = math.ceil(image.width / STICKERS_PER_CUBE)
    cube_rows = math.ceil(image.height / STICKERS_PER_CUBE)

    draw.text((50, 36), "CubeCanvas Build Guide", fill=INK, font=title_font)
    draw.text(
        (52, 92),
        "Overview map, chunk order, color key, and one printable instruction page per chunk.",
        fill=MUTED,
        font=subtitle_font,
    )

    stats = [
        f"Mosaic: {image.width} x {image.height} stickers",
        f"Chunks: {cols} x {rows} pages",
        f"Cube faces: about {cube_cols} x {cube_rows}",
        f"Chunk size: up to {CHUNK_SIZE} x {CHUNK_SIZE} stickers",
    ]

    for index, stat in enumerate(stats):
        x = 52 + index * 280
        stat_box = [x, 140, x + 250, 198]
        draw.rounded_rectangle(stat_box, radius=14, fill=PANEL, outline=PANEL_BORDER, width=2)
        draw_text_fit(draw, (stat_box[0] + 14, stat_box[1] + 10, stat_box[2] - 14, stat_box[3] - 10), stat, 20, bold=True)

    map_panel = (50, 230, 810, 980)
    side_panel = (840, 230, 1150, 980)
    draw_panel(draw, map_panel, "Full mosaic map")
    draw_panel(draw, side_panel, "Build details")

    placed = paste_fit(page, image, (80, 290, 780, 925))
    draw_chunk_grid(draw, image, placed, show_labels=True)

    draw_color_palette(draw, image, (870, 290, 1120, 930))

    return page


def draw_instruction_grid(draw, chunk, box):
    # Choose the largest sticker size that fits both width and height.
    available_w = box[2] - box[0]
    available_h = box[3] - box[1]
    cell = max(18, min(available_w // chunk.width, available_h // chunk.height))
    grid_w = cell * chunk.width
    grid_h = cell * chunk.height
    start_x = box[0] + (available_w - grid_w) // 2
    start_y = box[1] + (available_h - grid_h) // 2
    pixels = chunk.convert("RGB").load()

    for py in range(chunk.height):
        for px in range(chunk.width):
            x1 = start_x + px * cell
            y1 = start_y + py * cell
            draw.rectangle(
                [x1, y1, x1 + cell, y1 + cell],
                fill=pixels[px, py],
                outline=GRID_LINE,
                width=1,
            )

    for py in range(0, chunk.height + 1, STICKERS_PER_CUBE):
        y = start_y + py * cell
        draw.line([(start_x, y), (start_x + grid_w, y)], fill=CUBE_LINE, width=5)

    for px in range(0, chunk.width + 1, STICKERS_PER_CUBE):
        x = start_x + px * cell
        draw.line([(x, start_y), (x, start_y + grid_h)], fill=CUBE_LINE, width=5)

    draw.rectangle([start_x, start_y, start_x + grid_w, start_y + grid_h], outline=CUBE_LINE, width=6)

    return cell


def create_page(chunk, label, full_image, row, col):
    # Build one printable instruction page for a single mosaic chunk.
    page = Image.new("RGB", PAGE_SIZE, PAGE_BG)
    draw = ImageDraw.Draw(page)
    title_font = load_font(78, bold=True)
    meta_font = load_font(22)
    cols, rows = chunk_counts(full_image)

    draw.text((50, 34), f"Chunk {label}", fill=INK, font=title_font)
    draw.text(
        (55, 122),
        f"Page position: row {row + 1} of {rows}, column {col + 1} of {cols} | "
        f"Chunk size: {chunk.width} x {chunk.height} stickers",
        fill=MUTED,
        font=meta_font,
    )

    preview_panel = (50, 180, 395, 475)
    map_panel = (425, 180, 1150, 475)
    grid_panel = (50, 510, 1150, 1135)

    draw_panel(draw, preview_panel, "This chunk")
    draw_panel(draw, map_panel, "Where it goes")
    draw_panel(draw, grid_panel, "Sticker grid")

    paste_fit(page, chunk, (80, 240, 365, 445))

    placed = paste_fit(page, full_image, (455, 240, 1120, 445))
    draw_chunk_grid(draw, full_image, placed, current=(row, col), show_labels=True)

    draw_instruction_grid(draw, chunk, (85, 575, 1115, 1085))

    return page


def export_pdf(image):
    # Normalize to RGB so every PDF page can be saved without mode-specific errors.
    image = image.convert("RGB")
    chunk_cols, chunk_rows = chunk_counts(image)
    pages = [create_overview_page(image)]

    for row in range(chunk_rows):
        for col in range(chunk_cols):
            x1, y1, x2, y2 = chunk_bounds(image, col, row)
            chunk = image.crop((x1, y1, x2, y2))
            label = chunk_label(col, row)

            pages.append(
                create_page(
                    chunk=chunk,
                    label=label,
                    full_image=image,
                    row=row,
                    col=col,
                )
            )

    return pages
