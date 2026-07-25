from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np


def process_image(image, palette, cube_rows, cube_cols, mode, cube):
    image = image.convert("RGB")

    cube_size = 3

    if cube == "3x3":
        cube_size = 3
    elif cube == "4x4":
        cube_size = 4
    elif cube == "5x5":
        cube_size = 5

    global sticker_rows, sticker_cols

    sticker_rows = cube_rows * cube_size
    sticker_cols = cube_cols * cube_size

    if mode == "Nearest":
       return nearest(image, palette)

    elif mode == "Floyd-Steinberg":
        return floyd(image, palette)

    elif mode == "Ordered Bayer":
        return bayer(image, palette)

    elif mode == "Atkinson":
        return atkinson(image, palette)

    return None


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

def grayscale(image):
    return ImageOps.grayscale(image).convert("RGB")

def invert_image(image):
    return ImageOps.invert(image.convert("RGB"))

def white_balance(image):
    img = np.array(image).astype(np.float32)

    avg = img.mean(axis=(0,1))

    gray = avg.mean()

    scale = gray / avg

    img *= scale

    img = np.clip(img,0,255).astype(np.uint8)

    return Image.fromarray(img)

def gamma_correction(image, gamma):
    img = np.array(image).astype(np.float32) / 255

    img = np.power(img, gamma)

    img = np.clip(img * 255, 0, 255).astype(np.uint8)

    return Image.fromarray(img)


def apply_effects(
    image,
    brightness=1.0,
    contrast=1.0,
    saturation=1.0,
    sharpness=1.0,
    gamma=1.0,
    blur=0,
    flip_horizontal=False,
    flip_vertical=False,
    grayscale_img=False,
    invert_img=False,
    white_balance_img=False
):
    result = image.copy()

    if flip_horizontal:
        result = flip_x(result)

    if flip_vertical:
        result = flip_y(result)

    if grayscale_img:
        result = grayscale(result)

    if invert_img:
        result = invert_image(result)

    if white_balance_img:
        result = white_balance(result)

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

    result = gamma_correction(
        result,
        gamma
    )

    return result

def nearest_palette_color(pixel, palette):
    """
    pixel: RGB array of shape (3,)
    palette: numpy array of shape (N,3)
    """

    distances = np.sum((palette - pixel) ** 2, axis=1)
    return palette[np.argmin(distances)]

def nearest(image, palette):
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

def floyd(image, palette):
    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    small = np.array(small).astype(np.float32)

    # Cast the custom target color array elements into float32 to execute safe matrix arithmetic without clipping.
    palette = palette.astype(np.float32)

    # Output image that will contain only palette colours
    output = np.zeros_like(small)

    # Replace every sticker colour with the nearest
    # available Rubik colour using Floyd-Steinberg dithering.
    for r in range(sticker_rows):
        for c in range(sticker_cols):

            # Isolate the current pixel values which now include any color error distributed from earlier calculations.
            pixel = small[r, c]

            # Squared Euclidean distance to each palette colour
            distances = np.sum(
                (palette - pixel) ** 2,
                axis=1
            )

            # Choose the closest palette colour
            nearest_color = palette[np.argmin(distances)]

            # Assign the newly matched exact palette color directly into the final coordinate slot of the output matrix.
            output[r, c] = nearest_color

            # Calculate the exact difference between the original float pixel and the selected quantized palette color.
            error = pixel - nearest_color

            # Distribute 7/16ths of the quantization error to the immediately adjacent pixel situated on the right side.
            if c + 1 < sticker_cols:
                small[r, c + 1] += error * (7.0 / 16.0)

            # Route the remaining fractional error values into the row directly beneath the current pixel coordinate.
            if r + 1 < sticker_rows:

                # Distribute 3/16ths of the accumulated quantization error to the pixel sitting on the bottom-left diagonal.
                if c - 1 >= 0:
                    small[r + 1, c - 1] += error * (3.0 / 16.0)

                # Distribute 5/16ths of the accumulated quantization error straight down into the pixel directly underneath.
                small[r + 1, c] += error * (5.0 / 16.0)

                # Distribute the final 1/16th quantization error to the pixel situated on the bottom-right diagonal grid.
                if c + 1 < sticker_cols:
                    small[r + 1, c + 1] += error * (1.0 / 16.0)

    # Convert back to a PIL image for display
    return Image.fromarray(
        output.astype(np.uint8)
    )

def bayer(image, palette):
    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    BAYER_4 = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ], dtype=np.float32)

    # Normalize to [0,1]
    BAYER_4 = (BAYER_4 + 0.5) / 16.0

    img = np.array(small).astype(np.float32)

    h, w, _ = img.shape

    output = np.zeros_like(img)

    strength = 48  # Controls visibility of Bayer pattern

    for y in range(h):
        for x in range(w):
            pixel = img[y, x]

            threshold = BAYER_4[y % 4, x % 4]

            modified = pixel + (threshold - 0.5) * strength

            modified = np.clip(modified, 0, 255)

            output[y, x] = nearest_palette_color(modified, palette)

    return Image.fromarray(output.astype(np.uint8))

def atkinson(image, palette):
    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    img = np.array(small).astype(np.float32)

    h, w, _ = img.shape

    for y in range(h):
        for x in range(w):

            old = img[y, x]

            new = nearest_palette_color(old, palette)

            img[y, x] = new

            error = (old - new) / 8.0

            neighbours = [
                (1, 0),
                (2, 0),
                (-1, 1),
                (0, 1),
                (1, 1),
                (0, 2)
            ]

            for dx, dy in neighbours:

                nx = x + dx
                ny = y + dy

                if 0 <= nx < w and 0 <= ny < h:
                    img[ny, nx] += error

    img = np.clip(img, 0, 255)

    return Image.fromarray(img.astype(np.uint8))