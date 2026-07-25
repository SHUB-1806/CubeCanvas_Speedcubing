import cv2
import numpy as np
import math
import customtkinter as ctk
from tkinter import filedialog, messagebox

# ==========================================================
# 6 OFFICIAL RUBIK'S CUBE PALETTE COLORS
# ==========================================================
OFFICIAL_PALETTE = {
    "White": "#FFFFFF",
    "Yellow": "#FFD500",
    "Green": "#009E60",
    "Blue": "#0051BA",
    "Red": "#C41E3A",
    "Orange": "#FF5800"
}


def hex_to_rgb(hex_str):
    """Converts hex string (#RRGGBB) to an (R, G, B) tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    """Converts an (R, G, B) tuple to hex format (#RRGGBB)."""
    return '#%02x%02x%02x' % tuple(rgb[:3])


def closest_official_color(rgb):
    """
    Computes Euclidean color distance in RGB space to auto-select
    the best matching official Rubik's Cube color.
    """
    best_match = "White"
    min_dist = float("inf")
    
    for name, hex_val in OFFICIAL_PALETTE.items():
        ref_rgb = hex_to_rgb(hex_val)
        dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(rgb, ref_rgb)))
        if dist < min_dist:
            min_dist = dist
            best_match = name
            
    return best_match


def extract_3x3_colors(image_path):
    """
    Requirement 1 & 2:
    - Loads straight-on photo of a cube face using OpenCV (cv2).
    - Divides face into a 3x3 sticker grid.
    - Samples center 50% of each sticker cell to calculate pure average RGB
      without picking up black plastic bezels or gaps.
    - Reports average color as a hex code.
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    # OpenCV loads BGR by default -> Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, _ = img_rgb.shape

    cell_w = w / 3.0
    cell_h = h / 3.0

    extracted_stickers = []

    for row in range(3):
        for col in range(3):
            # Crop center 50% region of the cell (between 25% and 75%)
            x1 = int((col + 0.25) * cell_w)
            x2 = int((col + 0.75) * cell_w)
            y1 = int((row + 0.25) * cell_h)
            y2 = int((row + 0.75) * cell_h)

            sticker_crop = img_rgb[y1:y2, x1:x2]
            
            # Requirement 2: Extract average color of each sticker region
            avg_rgb = sticker_crop.mean(axis=(0, 1)).astype(int)
            hex_code = rgb_to_hex(avg_rgb)
            initial_match = closest_official_color(avg_rgb)

            extracted_stickers.append({
                "index": row * 3 + col + 1,
                "rgb": tuple(avg_rgb),
                "hex": hex_code,
                "assigned": initial_match
            })

    return extracted_stickers


class StickerExtractorWindow(ctk.CTkToplevel):
    """
    Requirements 3 & 4:
    - UI window allowing user to upload photo.
    - Displays extracted 9 sticker colors & hex codes.
    - Dropdowns to assign each sticker to 1 of 6 official palette colors.
    - Updates active palette upon saving.
    """
    def __init__(self, parent, on_palette_updated_callback):
        super().__init__(parent)
        self.title("Q7: Cube Sticker Color Extractor")
        self.geometry("680x750")
        self.grab_set()  # Focus mode window

        self.on_palette_updated_callback = on_palette_updated_callback
        self.extracted_data = []
        self.dropdown_vars = []

        self._build_ui()

    def _build_ui(self):
        # Header Controls Frame
        top_frame = ctk.CTkFrame(self)
        top_frame.pack(fill="x", padx=15, pady=15)

        self.upload_btn = ctk.CTkButton(
            top_frame, 
            text="📷 Upload Cube Face Photo", 
            command=self.load_image
        )
        self.upload_btn.pack(side="left", padx=10, pady=10)

        self.status_label = ctk.CTkLabel(
            top_frame, 
            text="Select a photo of a Rubik's Cube face.",
            anchor="w"
        )
        self.status_label.pack(side="left", padx=10, fill="x", expand=True)

        # Scrollable Grid Area for 3x3 stickers
        self.grid_scroll = ctk.CTkScrollableFrame(
            self, 
            label_text="Detected 3x3 Sticker Colors & Official Palette Assignments"
        )
        self.grid_scroll.pack(fill="both", expand=True, padx=15, pady=5)

        # Bottom Apply Button
        self.apply_btn = ctk.CTkButton(
            self, 
            text="✅ Update Active Palette", 
            fg_color="#16a34a", 
            hover_color="#15803d",
            command=self.apply_palette,
            state="disabled"
        )
        self.apply_btn.pack(pady=15)

    def load_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")]
        )
        if not file_path:
            return

        data = extract_3x3_colors(file_path)
        if data is None:
            messagebox.showerror("Error", "Could not load or process the selected image.")
            return

        self.extracted_data = data
        self.render_sticker_grid()
        self.apply_btn.configure(state="normal")
        self.status_label.configure(text="Extracted 9 stickers! Confirm assignments below:")

    def render_sticker_grid(self):
        # Clear existing widgets
        for child in self.grid_scroll.winfo_children():
            child.destroy()

        self.dropdown_vars.clear()

        # Render 3x3 Grid of extracted stickers
        for idx, item in enumerate(self.extracted_data):
            row = idx // 3
            col = idx % 3

            cell_frame = ctk.CTkFrame(self.grid_scroll, border_width=1, border_color="#cccccc")
            cell_frame.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            # Swatch displaying the extracted color
            swatch = ctk.CTkFrame(cell_frame, width=50, height=50, fg_color=item["hex"])
            swatch.pack(pady=(10, 4))

            # Extracted Hex code label
            hex_lbl = ctk.CTkLabel(cell_frame, text=item["hex"], font=("Consolas", 12, "bold"))
            hex_lbl.pack()

            # Requirement 3: Option Menu for 6 official palette colors
            var = ctk.StringVar(value=item["assigned"])
            dropdown = ctk.CTkOptionMenu(
                cell_frame,
                values=list(OFFICIAL_PALETTE.keys()),
                variable=var,
                width=115
            )
            dropdown.pack(pady=(4, 10))
            self.dropdown_vars.append(var)

    def apply_palette(self):
        """
        Requirement 4: Updates project's active color palette with user selections.
        Passes the RAW EXTRACTED PHOTO HEX CODES (e.g., #bc2319) mapped to their 
        assigned color categories into Page 2's expected row order:
        [White, Yellow, Green, Blue, Red, Orange]
        """
        CANONICAL_ORDER = ["White", "Yellow", "Green", "Blue", "Red", "Orange"]

        # Map assigned color category -> raw photo hex code detected
        detected_color_map = {}
        for item, var in zip(self.extracted_data, self.dropdown_vars):
            assigned_name = var.get()
            # Store the actual detected hex from the photo for this color label
            if assigned_name not in detected_color_map:
                detected_color_map[assigned_name] = item["hex"]

        # Build hex list in Page 2's required row order
        ordered_hex_list = []
        for color_name in CANONICAL_ORDER:
            # Use the photo's extracted hex, or fallback to official hex if that color wasn't on this face
            hex_val = detected_color_map.get(color_name, OFFICIAL_PALETTE[color_name])
            ordered_hex_list.append(hex_val)

        if self.on_palette_updated_callback:
            self.on_palette_updated_callback(ordered_hex_list)

        messagebox.showinfo("Success", "Palette updated")
        self.destroy()