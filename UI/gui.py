from pathlib import Path
import tkinter as tk
from tkinter import Canvas, Entry, Button, PhotoImage
from PIL import Image, ImageDraw, ImageFont, ImageTk

# Paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Admin\Desktop\build\assets\frame0")
FONT_PATH = ASSETS_PATH / "slkscr.ttf"

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Utility to render text as an image using Pillow
def render_text_image(text, font_path, size, color="#000000", bg=(255, 255, 255, 0)):
    font = ImageFont.truetype(str(font_path), size)
    dummy_img = Image.new("RGBA", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    text_width, text_height = dummy_draw.textsize(text, font=font)

    img = Image.new("RGBA", (text_width + 10, text_height + 10), bg)
    draw = ImageDraw.Draw(img)
    draw.text((5, 5), text, font=font, fill=color)
    return ImageTk.PhotoImage(img)

# Tkinter window setup
window = tk.Tk()
window.geometry("900x582")
window.configure(bg="#FFFFFF")
window.resizable(False, False)

canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=582,
    width=900,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

# Images
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(450.0, 291.0, image=image_image_1)

canvas.create_rectangle(
    461.12664794921875, 84.0, 871.2146301269531, 515.0,
    fill="#F8EFE0", outline="")

# Buttons
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(x=626.0, y=461.0, width=75.0, height=16.0)

button_image_2 = PhotoImage(file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(x=605.0, y=411.0, width=121.0, height=41.0)

# Entry 1
entry_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
canvas.create_image(672.72778, 366.82732, image=entry_image_1)
entry_1 = Entry(bd=0, bg="#E0E0E0", fg="#000716", highlightthickness=0)
entry_1.place(x=511.49505, y=345.91531, width=322.46545, height=39.82401)

# Entry 2
entry_image_2 = PhotoImage(file=relative_to_assets("entry_2.png"))
canvas.create_image(672.72778, 271.48273, image=entry_image_2)
entry_2 = Entry(bd=0, bg="#E0E0E0", fg="#000716", highlightthickness=0)
entry_2.place(x=514.49505, y=250.57072, width=316.46545, height=39.82401)

# Use Pillow-rendered Silkscreen text
label_login_img = render_text_image("LOGIN", FONT_PATH, 64, "#232323")
label_username_img = render_text_image("Username", FONT_PATH, 24, "#000000")
label_password_img = render_text_image("PASSWORD", FONT_PATH, 24, "#000000")

canvas.create_image(461, 128, image=label_login_img, anchor="nw")
canvas.create_image(506, 213, image=label_username_img, anchor="nw")
canvas.create_image(506, 308, image=label_password_img, anchor="nw")

# Extra image
image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(229.0, 314.0, image=image_image_2)

window.mainloop()
