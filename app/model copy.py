# libraries Import
from tkinter import *
import customtkinter

# Main Window Properties

window = Tk()
window.title("Tkinter")
window.geometry("800x350")
window.configure(bg="#FFFFFF")


radio_var = IntVar()

Button_id1 = customtkinter.CTkButton(
    master=window,
    text="Button1",
    font=("undefined", 14),
    text_color="#000000",
    hover=True,
    hover_color="#949494",
    height=30,
    width=95,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Button_id1.place(x=300, y=90)
RadioButton_id2 = customtkinter.CTkRadioButton(
    master=window,
    variable=radio_var,
    value=2,
    text="RadioButton2",
    text_color="#000000",
    border_color="#000000",
    fg_color="#808080",
    hover_color="#2F2F2F",
    )
RadioButton_id2.place(x=0, y=0)
Entry_id8 = customtkinter.CTkEntry(
    master=window,
    placeholder_text="Placeholder",
    placeholder_text_color="#454545",
    font=("Arial", 14),
    text_color="#000000",
    height=30,
    width=195,
    border_width=2,
    corner_radius=6,
    border_color="#000000",
    bg_color="#FFFFFF",
    fg_color="#F0F0F0",
    )
Entry_id8.place(x=190, y=150)



#run the main loop
window.mainloop()