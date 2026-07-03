from PIL import Image, ImageEnhance, ImageFilter
import numpy as np


def process_image(image, palette, cube_rows, cube_cols):
    image = image.convert("RGB")

    sticker_rows = cube_rows * 3
    sticker_cols = cube_cols * 3

    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    small = np.array(small, dtype=np.int32)

    palette = palette.astype(np.int32)

    output = np.zeros_like(small)

    for r in range(sticker_rows):
        for c in range(sticker_cols):
            pixel = small[r, c]

            distances = np.sum(
                (palette - pixel) ** 2,
                axis=1
            )

            output[r, c] = palette[np.argmin(distances)]

    return Image.fromarray(
        output.astype(np.uint8)
    )

def adjust_brightness(image, factor):
    enhancer = ImageEnhance.Brightness(image)

    return enhancer.enhance(factor)


def adjust_contrast(image, factor):
    enhancer = ImageEnhance.Contrast(image)

    return enhancer.enhance(factor)


def adjust_saturation(image, factor):
    enhancer = ImageEnhance.Color(image)

    return enhancer.enhance(factor)


def adjust_sharpness(image, factor):
    enhancer = ImageEnhance.Sharpness(image)

    return enhancer.enhance(factor)


def adjust_blur(image, radius):
    if radius <= 0:
        return image

    return image.filter(
        ImageFilter.GaussianBlur(radius)
    )


def flip_x(image):
    return image.transpose(
        Image.Transpose.FLIP_LEFT_RIGHT
    )


def flip_y(image):
    return image.transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )


def blur_mosaic(image, radius=1):
    if radius <= 0:
        return image

    return image.filter(
        ImageFilter.GaussianBlur(radius)
    )


def apply_effects(
    image,
    brightness=1.0,
    contrast=1.0,
    saturation=1.0,
    sharpness=1.0,
    blur=0,
    flip_horizontal=False,
    flip_vertical=False
):
    result = image.copy()

    if flip_horizontal:
        result = flip_x(result)

    if flip_vertical:
        result = flip_y(result)

    result = adjust_brightness(
        result,
        brightness
    )

    result = adjust_contrast(
        result,
        contrast
    )

    result = adjust_saturation(
        result,
        saturation
    )

    result = adjust_sharpness(
        result,
        sharpness
    )

    result = adjust_blur(
        result,
        blur
    )

    return result