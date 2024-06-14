import customtkinter as ctk
from tkinter import END
import re

calculation = ""

def append_to_calculation(symbol):
    global calculation
    calculation += str(symbol)
    input_field.configure(state="normal")
    input_field.delete(0, END)
    input_field.insert(END, calculation)
    input_field.configure(state="disable")

def evaluate():
    global calculation
    if calculation == "":
        input_field.configure(state="normal")
        input_field.insert(0, "enter a valid expression")
        input_field.configure(state="disable")
        return
    try:
        processed_calculation = preprocess_expression(calculation)
        result = str(eval(processed_calculation))
        input_field.configure(state="normal")
        input_field.delete(0, END)
        input_field.insert(END, result)
        input_field.configure(state="disable")
        calculation = result
    except Exception as e:
        print(type(e))
        if isinstance(e, ZeroDivisionError):
            input_field.configure(state="normal")
            input_field.delete(0, END)
            input_field.insert(END, "Cannot divide by zero")
            input_field.configure(state="disable")
            calculation = ""
        elif isinstance(e, ArithmeticError):
            input_field.configure(state="normal")
            input_field.delete(0, END)
            input_field.insert(END, e)
            input_field.configure(state="disable")
            calculation = ""
        else:
            input_field.configure(state="normal")
            input_field.delete(0, END)
            input_field.insert(END, "invalid expression")
            print(e)
            input_field.configure(state="disable")
            calculation = ""

def preprocess_expression(expr):
    expr = expr.replace(" ", "")
    expr = re.sub(r'(\d)(\()', r'\1*\2', expr)  
    expr = re.sub(r'(\))(\d)', r'\1*\2', expr)  
    expr = re.sub(r'(\))(\()', r'\1*\2', expr)  
    return expr

def clear_field():
    global calculation
    calculation = ""
    input_field.configure(state="normal")
    input_field.delete(0, END)
    input_field.configure(state="disable")

ctk.set_appearance_mode("dark")

app = ctk.CTk()
width = 450
height = 500
app.title("Calculator")
app.geometry(f"{width}x{height}")
app.resizable(0, 0)

app.grid_columnconfigure((0, 1, 2, 3), weight=1)
app.grid_rowconfigure(0, weight=10)
app.grid_rowconfigure(1, weight=90)

input_field = ctk.CTkEntry(app,
                           width=435,
                           height=130,
                           font=("JetBrainMono", 32),
                           bg_color="black",
                           fg_color="white",
                           text_color="black",
                           corner_radius=10,
                           border_width=2,
                           border_color="black",
                           state="disable",)
input_field.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

corner_color_dark = ["black", "black", "black", "black"]
corner_color_light = ["beige", "beige", "beige", "beige"]

button_frame = ctk.CTkFrame(app,
                            fg_color="white",
                            bg_color="black",
                            corner_radius=10,
                            width=width,
                            height=height-130,
                            border_width=2,
                            border_color="white",
                            background_corner_colors=corner_color_dark)
button_frame.grid(row=1, column=0, columnspan=4, rowspan=5, padx=10, pady=2, ipadx=10, ipady=3, sticky="nsew")

button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
button_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)

button_config = {
    "width": 100,
    "height": 100,
    "font": ("JetBrainMono", 30),
    "fg_color": "white",
    "text_color": "black",
    "corner_radius": 10,
    "hover_color": "lightgrey",
    "border_width": 1,
    "border_color": "grey",
    "background_corner_colors": corner_color_light
}


buttons = [
    [("CE", clear_field), ("(", lambda: append_to_calculation("(")), (")", lambda: append_to_calculation(")")), ("=", evaluate)],
    [("7", lambda: append_to_calculation("7")), ("8", lambda: append_to_calculation("8")), ("9", lambda: append_to_calculation("9")), ("/", lambda: append_to_calculation("/"))],
    [("4", lambda: append_to_calculation("4")), ("5", lambda: append_to_calculation("5")), ("6", lambda: append_to_calculation("6")), ("x", lambda: append_to_calculation("*"))],
    [("1", lambda: append_to_calculation("1")), ("2", lambda: append_to_calculation("2")), ("3", lambda: append_to_calculation("3")), ("-", lambda: append_to_calculation("-"))],
    [("0", lambda: append_to_calculation("0")), (".", lambda: append_to_calculation(".")), ("+/-", lambda: append_to_calculation("(-")), ("+", lambda: append_to_calculation("+"))]
]


for row_index, row in enumerate(buttons):
    for col_index, (text, command) in enumerate(row):
        button = ctk.CTkButton(button_frame, text=text, command=command, **button_config)
        button.grid(row=row_index + 1, column=col_index, pady=5, sticky="n")

app.mainloop()
