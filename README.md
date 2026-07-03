# CubeCanvas

CubeCanvas is an interactive image processing application that transforms photographs into Rubik's Cube mosaic art. It allows users to crop images, customize colors, apply artistic effects, and generate print-ready PDF instruction sheets for building the mosaic.

## Features

### Image Management
- **Import Images**: Load any image file from your system
- **Dynamic Resizing**: Automatically fit images to the viewing area with high-quality LANCZOS interpolation
- **Crosshair Guide**: Real-time crosshair cursor that follows mouse movement for precise selection

### Crop Selection
- **Interactive Cropping**: Click and drag to define your crop area
- **Aspect Ratio Constraint**: Automatically maintains the correct aspect ratio based on row/column settings
- **Visual Preview**: See the crop rectangle in real-time as you drag
- **Boundary Enforcement**: Crop boundaries are constrained within the image limits

### Image Effects and Editing
- **Brightness Control**: Adjust brightness from 0 to 2x
- **Contrast Enhancement**: Fine-tune contrast levels
- **Saturation Adjustment**: Control color intensity
- **Sharpness Filter**: Enhance or soften image details
- **Blur Effect**: Apply Gaussian blur with variable radius
- **Geometric Transforms**: Flip horizontally or vertically
- **Mosaic Blur**: Optional post-processing blur for the final mosaic output
- **Revert Changes**: Reset all effects to defaults with one click

### Color Customization
- **Rubik's Cube Palette**: Six customizable colors matching official Rubik's Cube sticker colors:
  - White, Yellow, Green, Blue, Red, Orange
- **Hex Color Support**: Edit colors using hex notation (e.g., `#FF5800`)
- **Live Preview**: Color boxes update as you type
- **Palette Persistence**: Your color choices are retained while editing

### Mosaic Generation
- **Configurable Grid**: Set custom row and column counts for the mosaic
- **Real-time Calculation**: Automatically calculates total number of cubes needed
- **Color Quantization**: Advanced pixel-to-color mapping using nearest-neighbor algorithm
- **Split Sticker Mode**: Each cube face is represented by 3x3 stickers (9 pixels total)

### PDF Export
- **Multi-page Instructions**: Generates comprehensive building instructions divided into manageable chunks
- **Overview Page**: First page shows the complete mosaic with labeled sections
- **Detailed Chunk Pages**: Individual instruction pages for each section featuring:
  - Large labeled preview of the chunk
  - Enlarged sticker diagram with custom colors
  - Mini-map showing current location within full mosaic
  - Thick grid lines indicating Rubik's Cube boundaries (every 3 stickers)
- **Print-Ready Format**: 900x900 pixel pages optimized for printing
- **Professional Layout**: Clean, organized instructions for easy assembly

## Architecture

### Core Modules

#### main.py
The main application controller managing:
- Multi-page UI (Page 1: Import, Page 2: Crop & Settings, Page 3: Effects & Export)
- Event handling (mouse tracking, cropping, canvas resizing)
- Image transformations and state management
- PDF export coordination

#### image_widgets.py
UI layout and widget construction:
- **Page 1**: Simple image import button
- **Page 2**: Cropping interface with color palette and grid controls
- **Page 3**: Effect controls (sliders, switches) and dual preview canvas
- Custom grid layouts for responsive design

#### image_processing.py
Image manipulation functions:
- `process_image()`: Quantizes image to palette colors with configurable grid
- `apply_effects()`: Applies brightness, contrast, saturation, sharpness, blur, and flip transformations
- `blur_mosaic()`: Post-processing blur for mosaic output
- Individual enhancement functions for each effect type

#### pdf_export.py
PDF generation pipeline:
- `create_overview_page()`: Generates the master index page with chunk layout
- `create_page()`: Generates individual instruction pages with:
  - Color-filled sticker diagram
  - Rubik's Cube boundary grid lines
  - Position indicator on mini-map
  - Chunk label and preview
- `export_pdf()`: Orchestrates multi-page PDF assembly from mosaic image

## Workflow

1. **Launch Application**: Opens to the home page with "Open Image" button
2. **Select Image**: Choose any image file from your system
3. **Crop and Configure**:
   - Position the image and draw crop rectangle
   - Set grid dimensions (rows x columns)
   - Customize Rubik's Cube sticker colors
4. **Apply Effects** (Page 3):
   - Adjust brightness, contrast, saturation, sharpness, blur
   - Apply geometric flips if desired
   - Toggle mosaic blur option
   - Preview changes in real-time on dual canvas
5. **Export**:
   - Click Export button
   - Choose save location and filename
   - PDF with full building instructions is generated

## Technologies

- Python 3.x
- tkinter / customtkinter: GUI framework with modern theming
- Pillow (PIL): Image processing and manipulation
- NumPy: Fast numerical array operations for color quantization
- ImageEnhance: Built-in image filter effects

## Requirements

```
customtkinter>=5.0
Pillow>=9.0
numpy>=1.20
```

## Usage

### Basic Setup
```bash
# Install dependencies
pip install customtkinter Pillow numpy

# Run the application
python main.py
```

### Creating a Rubik's Cube Mosaic

1. **Import**: Click "Open Image" to select your photo
2. **Crop**: Click and drag on the image to define your crop area (respects aspect ratio)
3. **Configure**: 
   - Enter desired rows and columns (e.g., 3x3 = 9 cubes)
   - Adjust sticker colors as needed
4. **Enhance**: On Page 3, fine-tune visual effects
5. **Export**: Generate PDF with step-by-step building instructions

## Key Data Structures

- **Palette**: NumPy array of RGB colors for quantization
- **Mosaic Image**: RGB image with width/height as (cols x 3) x (rows x 3) pixels
- **Crop Coordinates**: Normalized display coordinates converted to original image space
- **Effects State**: Stored as individual slider/switch values applied in sequence

## Development Timeline

This project was developed incrementally over 10 days:
- Days 1-3: Image import, display, and scaling
- Days 4-5: Multi-page UI and basic cropping
- Days 6-7: Crosshair and crop rectangle visualization
- Days 8-9: Mosaic generation with color effects
- Day 10: PDF export with comprehensive instructions
