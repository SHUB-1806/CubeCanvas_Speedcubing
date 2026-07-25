# COMMENT ON QUESTION 3
# Nearest Color produces flat, blocky color patches with harsh banding, best suited for simple graphics. Floyd–Steinberg creates the most realistic,
# photograph-like result by scattering fine, organic dots for smooth gradients. Ordered (Bayer) applies a rigid, repeating grid pattern that gives images a structured, 
# retro-arcade aesthetic. Meanwhile, Atkinson Dithering discards excess noise to deliver punchy contrast and crisp edge detail, preserving highlights and fine textures 
# without muddying the shadows.


from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import matplotlib.pyplot as plt


# --- Dithering & Quantization Algorithms ---

def find_closest_color(pixel, palette):
    """Finds the nearest palette color using Euclidean distance."""
    distances = np.sum((palette - pixel) ** 2, axis=1)
    return palette[np.argmin(distances)]


def dither_floyd_steinberg(arr, palette):
    """Floyd-Steinberg Error Diffusion Dithering."""
    h, w, _ = arr.shape
    img = arr.astype(np.float32)
    
    for r in range(h):
        for c in range(w):
            old_p = img[r, c].copy()
            new_p = find_closest_color(old_p, palette)
            img[r, c] = new_p
            err = old_p - new_p

            if c + 1 < w:
                img[r, c + 1] += err * (7.0 / 16.0)
            if r + 1 < h and c > 0:
                img[r + 1, c - 1] += err * (3.0 / 16.0)
            if r + 1 < h:
                img[r + 1, c] += err * (5.0 / 16.0)
            if r + 1 < h and c + 1 < w:
                img[r + 1, c + 1] += err * (1.0 / 16.0)

    return np.clip(img, 0, 255).astype(np.uint8)


def dither_bayer(arr, palette):
    """Ordered 4x4 Bayer Matrix Dithering."""
    h, w, _ = arr.shape
    img = arr.astype(np.float32)

    bayer_matrix = np.array([
        [ 0,  8,  2, 10],
        [12,  4, 14,  6],
        [ 3, 11,  1,  9],
        [15,  7, 13,  5]
    ], dtype=np.float32)

    threshold_map = (bayer_matrix / 16.0) - 0.5
    spread = 45.0  # Dithering threshold intensity

    out = np.zeros_like(arr, dtype=np.uint8)
    for r in range(h):
        for c in range(w):
            b_val = threshold_map[r % 4, c % 4] * spread
            adjusted = np.clip(img[r, c] + b_val, 0, 255)
            out[r, c] = find_closest_color(adjusted, palette)

    return out


def dither_atkinson(arr, palette):
    """Atkinson Error Diffusion Dithering (Preserves high contrast)."""
    h, w, _ = arr.shape
    img = arr.astype(np.float32)

    for r in range(h):
        for c in range(w):
            old_p = img[r, c].copy()
            new_p = find_closest_color(old_p, palette)
            img[r, c] = new_p
            err = old_p - new_p
            
            # Atkinson propagates 3/4 of the error across 6 neighbors
            e8 = err / 8.0
            if c + 1 < w:
                img[r, c + 1] += e8
            if c + 2 < w:
                img[r, c + 2] += e8
            if r + 1 < h and c - 1 >= 0:
                img[r + 1, c - 1] += e8
            if r + 1 < h:
                img[r + 1, c] += e8
            if r + 1 < h and c + 1 < w:
                img[r + 1, c + 1] += e8
            if r + 2 < h:
                img[r + 2, c] += e8

    return np.clip(img, 0, 255).astype(np.uint8)


# --- Core Pixelation Method ---



def process_image(image, palette, cube_rows, cube_cols, method="Nearest Color", cube_size=3):
    image = image.convert("RGB")

    sticker_rows = cube_rows * cube_size
    sticker_cols = cube_cols * cube_size

    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )
    small_arr = np.array(small, dtype=np.int32)
    palette = palette.astype(np.int32)

    if method == "Floyd-Steinberg":
        output_arr = dither_floyd_steinberg(small_arr, palette)
    elif method == "Ordered (Bayer)":
        output_arr = dither_bayer(small_arr, palette)
    elif method == "Atkinson Dithering":
        output_arr = dither_atkinson(small_arr, palette)
    else:  # Default "Nearest Color"
        output_arr = np.zeros_like(small_arr, dtype=np.uint8)
        for r in range(sticker_rows):
            for c in range(sticker_cols):
                pixel = small_arr[r, c]
                output_arr[r, c] = find_closest_color(pixel, palette)

    return Image.fromarray(output_arr)


# --- Image Adjustments & Filters ---

def adjust_brightness(image, factor):
    return ImageEnhance.Brightness(image).enhance(factor)

def adjust_contrast(image, factor):
    return ImageEnhance.Contrast(image).enhance(factor)

def adjust_saturation(image, factor):
    return ImageEnhance.Color(image).enhance(factor)

def adjust_sharpness(image, factor):
    return ImageEnhance.Sharpness(image).enhance(factor)

def adjust_blur(image, radius):
    if radius <= 0:
        return image
    return image.filter(ImageFilter.GaussianBlur(radius))

def flip_x(image):
    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

def flip_y(image):
    return image.transpose(Image.Transpose.FLIP_TOP_BOTTOM)

def blur_mosaic(image, radius=1):
    if radius <= 0:
        return image
    return image.filter(ImageFilter.GaussianBlur(radius))

def apply_invert(image):
    return ImageOps.invert(image.convert("RGB"))

def apply_grayscale(image):
    return ImageOps.grayscale(image).convert("RGB")

def apply_gamma(image, gamma=1.0):
    if gamma == 1.0 or gamma <= 0:
        return image
    arr = np.array(image, dtype=np.float32) / 255.0
    corrected = np.power(arr, gamma) * 255.0
    return Image.fromarray(np.clip(corrected, 0, 255).astype(np.uint8))

def apply_white_balance(image):
    arr = np.array(image, dtype=np.float32)
    r_mean = np.mean(arr[:, :, 0])
    g_mean = np.mean(arr[:, :, 1])
    b_mean = np.mean(arr[:, :, 2])
    if r_mean == 0 or b_mean == 0:
        return image
    arr[:, :, 0] *= (g_mean / r_mean)
    arr[:, :, 2] *= (g_mean / b_mean)
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))

def apply_effects(
    image,
    brightness=1.0,
    contrast=1.0,
    saturation=1.0,
    sharpness=1.0,
    blur=0,
    gamma=1.0,
    flip_horizontal=False,
    flip_vertical=False,
    invert=False,
    grayscale=False,
    white_balance=False
):
    result = image.copy()
    if flip_horizontal:
        result = flip_x(result)
    if flip_vertical:
        result = flip_y(result)
    if invert:
        result = apply_invert(result)
    if grayscale:
        result = apply_grayscale(result)
    if white_balance:
        result = apply_white_balance(result)

    result = adjust_brightness(result, brightness)
    result = adjust_contrast(result, contrast)
    result = adjust_saturation(result, saturation)
    result = adjust_sharpness(result, sharpness)
    result = adjust_blur(result, blur)
    result = apply_gamma(result, gamma)
    return result

def show_histogram(image):
    if image is None:
        return

    # Ensure image is in RGB mode
    image = image.convert("RGB")
    r, g, b = image.split()

    # 1. Target the named window FIRST, then clear previous drawings
    plt.figure("RGB Histogram Viewer")
    plt.clf()

    # 2. Plot individual color channel distributions
    plt.plot(r.histogram(), color='red', label='Red')
    plt.plot(g.histogram(), color='green', label='Green')
    plt.plot(b.histogram(), color='blue', label='Blue')

    # 3. Apply labels, grid, and exact 8-bit pixel bounds
    plt.title("RGB Channel Intensity Histogram")
    plt.xlabel("Pixel Intensity (0 - 255)")
    plt.ylabel("Pixel Count")
    plt.xlim([0, 256])
    plt.legend(loc="upper right")
    plt.grid(True, linestyle="--", alpha=0.5)

    # 4. Non-blocking call prevents Tkinter GUI freeze
    plt.show(block=False)