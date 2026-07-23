from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import matplotlib.pyplot as plt

def find_nearest_color(pixel, palette):
    distances = np.sum((palette - pixel) ** 2, axis=1)
    return palette[np.argmin(distances)]


def process_image(
    image,
    palette,
    cube_rows,
    cube_cols,
    method="Nearest Color",
    cube_size=3,
):
    image = image.convert("RGB")

    sticker_rows = cube_rows * cube_size
    sticker_cols = cube_cols * cube_size

    small = image.resize(
        (sticker_cols, sticker_rows), Image.Resampling.LANCZOS
    )

    small_np = np.array(small, dtype=np.float32)
    palette = palette.astype(np.float32)
    h, w, _ = small_np.shape
    output = np.zeros_like(small_np)

    if method == "Nearest Color":
        for r in range(h):
            for c in range(w):
                output[r, c] = find_nearest_color(small_np[r, c], palette)

    elif method == "Floyd-Steinberg":
        img_copy = small_np.copy()
        for y in range(h):
            for x in range(w):
                old_p = img_copy[y, x].copy()
                new_p = find_nearest_color(old_p, palette)
                img_copy[y, x] = new_p
                err = old_p - new_p

                if x + 1 < w:
                    img_copy[y, x + 1] += err * (7 / 16)
                if y + 1 < h:
                    if x > 0:
                        img_copy[y + 1, x - 1] += err * (3 / 16)
                    img_copy[y + 1, x] += err * (5 / 16)
                    if x + 1 < w:
                        img_copy[y + 1, x + 1] += err * (1 / 16)
        output = img_copy

    elif method == "Bayer Matrix":
        bayer_4x4 = (
            np.array(
                [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]],
                dtype=np.float32,
            )
            / 16.0
            - 0.5
        ) * 32.0

        for y in range(h):
            for x in range(w):
                offset = bayer_4x4[y % 4, x % 4]
                mod_p = np.clip(small_np[y, x] + offset, 0, 255)
                output[y, x] = find_nearest_color(mod_p, palette)

    elif method == "Atkinson":
        img_copy = small_np.copy()
        for y in range(h):
            for x in range(w):
                old_p = img_copy[y, x].copy()
                new_p = find_nearest_color(old_p, palette)
                img_copy[y, x] = new_p
                err = (old_p - new_p) / 8.0

                if x + 1 < w:
                    img_copy[y, x + 1] += err
                if x + 2 < w:
                    img_copy[y, x + 2] += err
                if y + 1 < h:
                    if x > 0:
                        img_copy[y + 1, x - 1] += err
                    img_copy[y + 1, x] += err
                    if x + 1 < w:
                        img_copy[y + 1, x + 1] += err
                if y + 2 < h:
                    img_copy[y + 2, x] += err
        output = img_copy

    return Image.fromarray(np.clip(output, 0, 255).astype(np.uint8))

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

#Question 1
def show_histogram(image):
    import matplotlib.pyplot as plt

    img_np = np.array(image.convert("RGB"))
    r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]

    plt.figure(figsize=(7, 3.5))
    plt.title("RGB Channel Intensity Histogram")
    plt.xlabel("Pixel Intensity (0-255)")
    plt.ylabel("Pixel Count")

    plt.hist(r.ravel(), bins=256, color="red", alpha=0.5, label="Red")
    plt.hist(g.ravel(), bins=256, color="green", alpha=0.5, label="Green")
    plt.hist(b.ravel(), bins=256, color="blue", alpha=0.5, label="Blue")

    plt.xlim([0, 256])
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.show()

#Question 2
def apply_invert(image):
    from PIL import ImageOps

    return ImageOps.invert(image.convert("RGB"))


def apply_white_balance(image):
    img_np = np.array(image.convert("RGB"), dtype=np.float32)
    avg_r, avg_g, avg_b = (
        np.mean(img_np[:, :, 0]),
        np.mean(img_np[:, :, 1]),
        np.mean(img_np[:, :, 2]),
    )
    gray_avg = (avg_r + avg_g + avg_b) / 3.0

    img_np[:, :, 0] = np.clip(
        img_np[:, :, 0] * (gray_avg / (avg_r + 1e-5)), 0, 255
    )
    img_np[:, :, 1] = np.clip(
        img_np[:, :, 1] * (gray_avg / (avg_g + 1e-5)), 0, 255
    )
    img_np[:, :, 2] = np.clip(
        img_np[:, :, 2] * (gray_avg / (avg_b + 1e-5)), 0, 255
    )

    return Image.fromarray(img_np.astype(np.uint8))


def apply_gamma(image, gamma=1.8):
    if gamma <= 0:
        gamma = 1.0
    inv_gamma = 1.0 / gamma
    table = np.array(
        [((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]
    ).astype("uint8")
    img_np = np.array(image.convert("RGB"))
    return Image.fromarray(table[img_np])


def apply_posterize(image, bits=3):
    from PIL import ImageOps

    return ImageOps.posterize(image.convert("RGB"), bits)    