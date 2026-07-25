from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import tkinter as tk

BAYER_4X4 = np.array([
    [0, 8, 2,10],
    [12,4,14,6],
    [3,11,1,9],
    [15,7,13,5]
]) / 16.0

def process_image(image, palette, cube_rows, cube_cols, algorithm="nearest"):
    image = image.convert("RGB")

    sticker_rows = cube_rows * 3
    sticker_cols = cube_cols * 3

    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    working = np.array(small, dtype=np.float32)
    palette = palette.astype(np.float32)

    output = np.zeros_like(working)

    for r in range(sticker_rows):
        for c in range(sticker_cols):

            pixel = working[r, c].copy()

            if algorithm == "ordered":
                threshold = (BAYER_4X4[r % 4, c % 4] - 0.5) * 32
                pixel = np.clip(pixel + threshold, 0, 255)

            distances = np.sum((palette - pixel) ** 2, axis=1)
            nearest = palette[np.argmin(distances)]

            output[r, c] = nearest

            if algorithm == "atkinson":

                error = (pixel - nearest) / 8.0

                neighbours = [
                    (r, c + 1),
                    (r, c + 2),
                    (r + 1, c - 1),
                    (r + 1, c),
                    (r + 1, c + 1),
                    (r + 2, c)
                ]

                for rr, cc in neighbours:
                    if 0 <= rr < sticker_rows and 0 <= cc < sticker_cols:
                        working[rr, cc] += error

            if algorithm == "floyd":

                error = pixel - nearest

                diffusion = [
                    (0, 1, 7 / 16),
                    (1, -1, 3 / 16),
                    (1, 0, 5 / 16),
                    (1, 1, 1 / 16),
                ]

                for dr, dc, weight in diffusion:
                    rr = r + dr
                    cc = c + dc

                    if 0 <= rr < sticker_rows and 0 <= cc < sticker_cols:
                        working[rr, cc] += error * weight
            
    output = np.clip(output, 0, 255)

    return Image.fromarray(output.astype(np.uint8))
    

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

def invert_image(image):
    return ImageOps.invert(image.convert("RGB"))

def white_balance(image):
    img = np.array(image).astype(np.float32)

    mean_r = np.mean(img[:, :, 0])
    mean_g = np.mean(img[:, :, 1])
    mean_b = np.mean(img[:, :, 2])

    mean_gray = (mean_r + mean_g + mean_b) / 3

    img[:, :, 0] *= mean_gray / mean_r
    img[:, :, 1] *= mean_gray / mean_g
    img[:, :, 2] *= mean_gray / mean_b

    img = np.clip(img, 0, 255).astype(np.uint8)

    return Image.fromarray(img)

def gamma_correction(image, gamma=1.5):
    img = np.array(image).astype(np.float32) / 255.0

    img = np.power(img, gamma)

    img = (img * 255).clip(0, 255).astype(np.uint8)

    return Image.fromarray(img)

def grayscale(image):
    return image.convert("L").convert("RGB")

def apply_effects(
    image,
    brightness=1.0,
    contrast=1.0,
    saturation=1.0,
    sharpness=1.0,
    blur=0,
    flip_horizontal=False,
    flip_vertical=False,
    negative=False,
    white_balance_enabled=False,
    gamma_enabled=False,
    grayscale_enabled=False
):
    result = image.copy()

    if flip_horizontal:
        result = flip_x(result)

    if flip_vertical:
        result = flip_y(result)

    if negative:
        result = invert_image(result)

    if white_balance_enabled:
        result = white_balance(result)

    if gamma_enabled:
        result = gamma_correction(result)

    if grayscale_enabled:
       result = grayscale(result)   
    
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


def show_histogram(image):
    image = image.convert("RGB")
    pixels = np.array(image)

    red = pixels[:, :, 0]
    green = pixels[:, :, 1]
    blue = pixels[:, :, 2]

    red_hist = np.bincount(red.flatten(), minlength=256)
    green_hist = np.bincount(green.flatten(), minlength=256)
    blue_hist = np.bincount(blue.flatten(), minlength=256)

    window = tk.Toplevel()
    window.title("RGB Histogram")

    canvas = tk.Canvas(window, width=512, height=300, bg="white")
    canvas.pack()

    max_value = max(red_hist.max(), green_hist.max(), blue_hist.max())

    for i in range(256):
        x = i * 2

        r_height = int((red_hist[i] / max_value) * 280)
        g_height = int((green_hist[i] / max_value) * 280)
        b_height = int((blue_hist[i] / max_value) * 280)

        canvas.create_line(x, 300, x, 300 - r_height, fill="red")
        canvas.create_line(x, 300, x, 300 - g_height, fill="green")
        canvas.create_line(x, 300, x, 300 - b_height, fill="blue")