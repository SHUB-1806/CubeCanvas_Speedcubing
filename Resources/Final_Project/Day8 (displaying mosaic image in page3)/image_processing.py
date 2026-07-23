# from PIL import Image
# import numpy as np


# def process_image(image, palette, cube_rows, cube_cols):
#     """
#     Convert an image into a Rubik's Cube mosaic.

#     Each Rubik's cube has a 3×3 face, so an n×m cube layout
#     actually corresponds to a (3n)×(3m) sticker grid.
#     """

#     # Force conversion of the incoming graphic into a standard red, green, and blue three-channel image layer.
#     image = image.convert("RGB")

#     # Convert cube dimensions into sticker dimensions
#     # Example: 40×30 cubes → 120×90 stickers
#     sticker_rows = cube_rows * 3
#     sticker_cols = cube_cols * 3

#     # Resize the image so that each pixel represents
#     # one Rubik sticker
#     small = image.resize(
#         (sticker_cols, sticker_rows),
#         Image.Resampling.LANCZOS
#     )

#     # Convert to NumPy for faster calculations
#     # int32 prevents overflow during subtraction
#     small = np.array(small).astype(np.int32)

#     # Cast the custom target color array elements into signed 32-bit integers to execute safe matrix arithmetic.
#     palette = palette.astype(np.int32)

#     # Output image that will contain only palette colours
#     output = np.zeros_like(small)

#     # Replace every sticker colour with the nearest
#     # available Rubik colour
#     for r in range(sticker_rows):
#         for c in range(sticker_cols):

#             pixel = small[r, c]

#             # Squared Euclidean distance to each palette colour
#             distances = np.sum(
#                 (palette - pixel) ** 2,
#                 axis=1
#             )

#             # Choose the closest palette colour (argmin is to choose the colour with minimum difference)
#             output[r, c] = palette[np.argmin(distances)]

#     # Convert back to a PIL image for display
#     return Image.fromarray(
#         output.astype(np.uint8)
#     )



from PIL import Image
import numpy as np


def process_image(image, palette, cube_rows, cube_cols):
    """
    Convert an image into a Rubik's Cube mosaic.

    Each Rubik's cube has a 3×3 face, so an n×m cube layout
    actually corresponds to a (3n)×(3m) sticker grid.
    """

    # Force conversion of the incoming graphic into a standard red, green, and blue three-channel image layer.
    image = image.convert("RGB")

    # Convert cube dimensions into sticker dimensions
    # Example: 40×30 cubes → 120×90 stickers
    sticker_rows = cube_rows * 3
    sticker_cols = cube_cols * 3

    # Resize the image so that each pixel represents
    # one Rubik sticker
    small = image.resize(
        (sticker_cols, sticker_rows),
        Image.Resampling.LANCZOS
    )

    # Convert the resized image array into float32 to prevent data loss when propagating fractional decimal errors.
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