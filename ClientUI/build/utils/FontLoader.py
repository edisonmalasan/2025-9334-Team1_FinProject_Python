from tkinter import font as tkfont
from PIL import ImageFont, Image
from pathlib import Path
import warnings

class FontLoader:
    def __init__(self, assets_path: Path):
        self.assets_path = assets_path
        self.fonts = {} 

    def load_tk_font(
        self,
        name: str,
        family: str,
        size: int,
        weight: str = "normal",
        slant: str = "roman"
    ) -> tkfont.Font:
        """Load a Tkinter-compatible font (must be installed on system)."""
        try:
            tk_font = tkfont.Font(
                family=family,
                size=size,
                weight=weight,
                slant=slant
            )
            self.fonts[name] = tk_font
            return tk_font
        except Exception as e:
            warnings.warn(f"Failed to load Tk font '{family}': {e}. Using fallback.")
            return tkfont.Font(family="Arial", size=size, weight=weight)

    def load_pil_font(
        self,
        name: str,
        font_file: str,
        size: int
    ) -> ImageFont.FreeTypeFont:
        """Load a custom font file (for PIL-based rendering)."""
        try:
            pil_font = ImageFont.truetype(str(self.assets_path / "fonts" / font_file), size)
            self.fonts[name] = pil_font
            return pil_font
        except IOError as e:
            warnings.warn(f"Failed to load PIL font '{font_file}': {e}")
            return None

    def get_font(self, name: str):
        """Retrieve a loaded font by name."""
        return self.fonts.get(name)