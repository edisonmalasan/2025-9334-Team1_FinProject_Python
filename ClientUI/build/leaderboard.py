from pathlib import Path
from tkinter import Tk, Canvas, PhotoImage, Button
from tkinter.ttk import Treeview, Style
import tkinter.font as tkfont

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\paulp\VSCODE_REPO\2025-9334-team1_finproject_python\ClientUI\build\assets\leaderboard")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

window = Tk()
window.geometry("985x589")
window.configure(bg="#FFFFFF")

#canvas
canvas = Canvas(
    window,
    bg="#FFFFFF",
    height=589,
    width=985,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)
canvas.place(x=0, y=0)

#bg img
image_image_1 = PhotoImage(file=relative_to_assets("image_1.png"))
canvas.create_image(300.0, 500.0, image=image_image_1)

image_image_2 = PhotoImage(file=relative_to_assets("image_2.png"))
canvas.create_image(493.0, 72.0, image=image_image_2)

#leaderboard title
canvas.create_text(
    300.0,
    118.0,
    anchor="nw",
    text="LEADERBOARD",
    fill="#FFFFFF",
    font=("Silkscreen Regular", 36)
)

#table
style = Style()
style.configure("Treeview.Heading", font=("Silkscreen Regular", 15), foreground="#FFAB24")
style.configure("Treeview", font=("Montserrat Regular", 10), foreground="#FFFFFF", background="#232323")
style.map("Treeview", background=[("selected", "#FFAB24")])

table = Treeview(
    window,
    columns=("rank", "username", "points"),
    show="headings",
    height=10,
    style="Custom.Treeview"
)

table.tag_bind('leaderboard_table')

#columns
table.column("rank", width=100, anchor="center")
table.column("username", width=400, anchor="center")
table.column("points", width=100, anchor="center")

#headings
table.heading("rank", text="RANK")
table.heading("username", text="USERNAME")
table.heading("points", text="POINTS")

table.place(x=100, y=200, width=785, height=300)

#sample data
leaderboard_data = [
    ("1", "PlayerOne", "1500"),
    ("2", "PlayerTwo", "1450"),
    ("3", "PlayerThree", "1400"),
    ("4", "PlayerFour", "1350"),
    ("5", "PlayerFive", "1300"),
]

for item in leaderboard_data:
    table.insert("", "end", values=item)

#button
button_image_1 = PhotoImage(file=relative_to_assets("button_1.png"))
button_1 = Button(
    window,  # Changed from canvas to window
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat",
    bg="#232323"
)
button_1.place(
    x=445,
    y=536,
    width=95,
    height=28
)

window.resizable(False, False)
window.mainloop()