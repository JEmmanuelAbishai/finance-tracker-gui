import os
import sys
import platform
import ctypes


def get_font_dir():
    """Resolve the fonts folder relative to this file."""
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base, "assets", "fonts")


def load_custom_fonts():
    """Register the JetBrains Mono .ttf files with the OS for this process."""
    font_dir = get_font_dir()
    font_files = [
        "JetBrainsMono-Regular.ttf",
        "JetBrainsMono-Bold.ttf",
        "JetBrainsMono-Italic.ttf",
    ]

    system = platform.system()

    if system == "Windows":
        FR_PRIVATE = 0x10
        for f in font_files:
            path = os.path.join(font_dir, f)
            if os.path.exists(path):
                ctypes.windll.gdi32.AddFontResourceExW(path, FR_PRIVATE, 0)
            else:
                print(f"[fonts] Warning: missing font file {path}")

    elif system == "Darwin":
        for f in font_files:
            path = os.path.join(font_dir, f)
            if not os.path.exists(path):
                print(f"[fonts] Warning: missing font file {path}")
        print("[fonts] Note: on macOS, install these .ttf files to "
              "~/Library/Fonts for the font to be available to Tk.")

    elif system == "Linux":
        target_dir = os.path.expanduser("~/.local/share/fonts")
        os.makedirs(target_dir, exist_ok=True)
        copied_any = False
        for f in font_files:
            src = os.path.join(font_dir, f)
            dst = os.path.join(target_dir, f)
            if os.path.exists(src) and not os.path.exists(dst):
                import shutil
                shutil.copy2(src, dst)
                copied_any = True
            elif not os.path.exists(src):
                print(f"[fonts] Warning: missing font file {src}")
        if copied_any:
            os.system("fc-cache -f >/dev/null 2>&1")