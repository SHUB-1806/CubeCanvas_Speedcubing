from PIL import Image, ImageEnhance, ImageFilter
import numpy as np


def process_image(image, palette, cube_rows, cube_cols):
    # Force conversion of the incoming graphic into a standard red, green, and blue three-channel image layer.
    image = image.convert("RGB")

    # Convert the user-defined cube matrix dimensions directly into detailed visual grid sticker dimensions.
    sticker_rows = cube_rows * 3
    sticker_cols = cube_cols * 3

    # Downsample the target photo asset to match the total pixel grid specifications using Lanczos filters.
    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    # Cast the resized image matrix data into signed 32-bit integers to prevent runtime calculation overflows.
    small = np.array(small, dtype=np.int32)

    # Convert the user color array configuration records into signed 32-bit integers for matrix processing.
    palette = palette.astype(np.int32)

    # Instantiate a clean blank target array layer matching the small photo dimensions to store final colors.
    output = np.zeros_like(small)

    # Loop row by row through every single sticker coordinate index position inside the scaled-down grid canvas.
    for r in range(sticker_rows):
        for c in range(sticker_cols):
            # Isolate the current individual target pixel coordinate vector data from the active image array.
            pixel = small[r, c]

            # Compute the squared Euclidean spatial distances mapping the active target pixel against all colors.
            distances = np.sum(
                (palette - pixel) ** 2,
                axis=1
            )

            # Match the pixel to its nearest neighbor color palette index and commit the color to output maps.
            output[r, c] = palette[np.argmin(distances)]

    # Transform the final quantized integer color array back into a standard format PIL Image object handler.
    return Image.fromarray(
        output.astype(np.uint8)
    )

def adjust_brightness(image, factor):
    """
    Adjust image brightness.

    Parameters
    ----------
    image : PIL.Image
        Input image.

    factor : float
        0   -> completely black
        1   -> original image
        >1  -> brighter image

    Returns
    -------
    PIL.Image
        Brightness-adjusted image.
    """

    # Instantiate a core Pillow enhancement class worker instance tasked with managing image exposure channels.
    enhancer = ImageEnhance.Brightness(image)

    # Apply the custom floating point multiplier to modify structural exposure values on the target graphic.
    return enhancer.enhance(factor)


def adjust_contrast(image, factor):
    """
    Adjust image contrast.

    Parameters
    ----------
    image : PIL.Image
        Input image.

    factor : float
        0   -> flat gray image
        1   -> original image
        >1  -> stronger contrast

    Returns
    -------
    PIL.Image
        Contrast-adjusted image.
    """

    # Instantiate a core Pillow enhancement class worker instance tasked with managing tone distance variances.
    enhancer = ImageEnhance.Contrast(image)

    # Execute the numeric scaling transformation routine to widen or narrow tonal range limits on the image.
    return enhancer.enhance(factor)


def adjust_saturation(image, factor):
    """
    Adjust image colour saturation.

    Parameters
    ----------
    image : PIL.Image
        Input image.

    factor : float
        0   -> grayscale image
        1   -> original image
        >1  -> more vivid colours

    Returns
    -------
    PIL.Image
        Saturation-adjusted image.
    """

    # Instantiate a core Pillow enhancement class worker instance tasked with modifying overall color intensity.
    enhancer = ImageEnhance.Color(image)

    # Process the image matrix data with the input multiplier coefficient to dilute or enrich color profiles.
    return enhancer.enhance(factor)


def adjust_sharpness(image, factor):
    """
    Adjust image sharpness.

    Parameters
    ----------
    image : PIL.Image
        Input image.

    factor : float
        0   -> soft/blurred appearance
        1   -> original image
        >1  -> sharper image

    Returns
    -------
    PIL.Image
        Sharpness-adjusted image.
    """

    # Instantiate a core Pillow enhancement class worker instance tasked with evaluating localized pixel edges.
    enhancer = ImageEnhance.Sharpness(image)

    # Run edge-discrimination enhancement routines on the graphic asset using the targeted floating multiplier.
    return enhancer.enhance(factor)


def adjust_blur(image, radius):
    """
    Apply Gaussian blur to an image.

    Parameters
    ----------
    image : PIL.Image
        Input image.

    radius : float
        0 or less -> no blur
        Larger values produce stronger blur.

    Returns
    -------
    PIL.Image
        Blurred image.
    """

    # Intercept processing configurations early if the radius value does not register a positive distribution.
    if radius <= 0:
        return image

    # Pass a structured Gaussian matrix convolution mathematical filter directly over the target image asset.
    return image.filter(
        ImageFilter.GaussianBlur(radius)
    )


def flip_x(image):
    """
    Flip an image horizontally.

    The left and right sides are swapped.

    Returns
    -------
    PIL.Image
        Horizontally flipped image.
    """

    # Transpose the underlying pixel index structures symmetrically along the central vertical canvas axis map.
    return image.transpose(
        Image.Transpose.FLIP_LEFT_RIGHT
    )


def flip_y(image):
    """
    Flip an image vertically.

    The top and bottom sides are swapped.

    Returns
    -------
    PIL.Image
        Vertically flipped image.
    """

    # Transpose the underlying pixel index structures symmetrically along the central horizontal canvas axis map.
    return image.transpose(
        Image.Transpose.FLIP_TOP_BOTTOM
    )


def blur_mosaic(image, radius=1):
    """
    Apply blur only to the generated Rubik mosaic.

    This effect is applied after the mosaic has
    been created and does not affect the original
    preview image.

    Parameters
    ----------
    image : PIL.Image
        Mosaic image.

    radius : float
        Blur strength.

    Returns
    -------
    PIL.Image
        Blurred mosaic image.
    """

    # Safeguard calculations by exiting immediately if the blur evaluation step properties drop to zero or below.
    if radius <= 0:
        return image

    # Apply a low-pass Gaussian smoothing filter layer exclusively over the completed blocky mosaic image data.
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
    """
    Apply all preview effects to an image.

    Effects are applied to a copy of the image so
    the original remains unchanged.

    Order of operations:
        1. Horizontal flip
        2. Vertical flip
        3. Brightness
        4. Contrast
        5. Saturation
        6. Sharpness
        7. Blur

    Parameters
    ----------
    image : PIL.Image
        Source image.

    brightness : float
        Brightness multiplier.

    contrast : float
        Contrast multiplier.

    saturation : float
        Saturation multiplier.

    sharpness : float
        Sharpness multiplier.

    blur : float
        Gaussian blur radius.

    flip_horizontal : bool
        Whether to mirror the image left-to-right.

    flip_vertical : bool
        Whether to mirror the image top-to-bottom.

    Returns
    -------
    PIL.Image
        Image with all selected effects applied.
    """

    # Work on a copy to preserve the original image
    result = image.copy()

    #
    # Apply geometric transformations first
    #
    if flip_horizontal:
        result = flip_x(result)

    if flip_vertical:
        result = flip_y(result)

    #
    # Apply colour and detail adjustments
    #
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

    #
    # Apply blur last so that it affects
    # the final appearance of all previous effects
    #
    result = adjust_blur(
        result,
        blur
    )

    return result