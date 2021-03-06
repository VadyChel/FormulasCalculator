import os
import re
from tkinter import Tk, Text, Canvas, messagebox, Checkbutton, BooleanVar
from tkinter.ttk import Label, Entry, Style, Combobox, Button

from PIL import ImageTk, Image

from core.exceptions import CalculationException, SyntaxException
from core.formulas_analyzer import draw_graph


class App(Tk):
    def __init__(self, window):
        self.window = window

        # GUI Elements
        self.xmin: Entry = None
        self.xmax: Entry = None

        # Configure main style
        self.style: Style = Style()
        self.style.configure(
            "TLabel", font=("Segoe UI", 10, 'bold'), foreground="#333333"
        )
        self.style.configure(
            "TEntry", font=("Segoe UI", 10), foreground="#333333"
        )
        self.style.configure(
            "TButton",
            font=("Segoe UI", 16),
            foreground="#444444",
            background='#ffffff'
        )
        self.style.map('TButton', background=[('active', '#ffffff'), ('disabled', '#111111')])
        self.style.configure(
            "TCombobox", font=("Segoe UI", 16), foreground="#444444"
        )
        self.vcmd = (
            self.window.register(self.validate_numbers),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'
        )
        # Create window
        self.create_window()

    def validate_numbers(self, d, i, P, s, edited_text, v, V, W):
        # d = Type of action (1=insert, 0=delete, -1 for others)
        # i = index of char string to be inserted/deleted, or -1
        # P = value of the entry if the edit is allowed
        # s = value of entry prior to editing
        # edited_text = the text string being inserted or deleted, if any
        # v = the type of validation that is currently set
        # V = the type of validation that triggered the callback
        #      (key, focusin, focusout, forced)
        # W = the tk name of the widget

        # Check if string is number or number with - on the front
        if edited_text.isdigit() or re.match('-?\d+', edited_text) is not None or edited_text == '-':
            return True

        return False

    def create_window(self):
        self.window.title("FormulasCalculator")
        # self.window.iconbitmap(os.path.dirname(os.path.abspath(__file__)) + "/icon.ico")
        self.window.geometry("890x500")
        self.window.resizable(width=False, height=False)

        self.create_gui()

    def create_gui(self):
        # Xmin and xmax inputs and labels
        self.xmin_label = Label(
            self.window,
            text='X minimum'
        )
        self.xmax_label = Label(
            self.window,
            text='X maximum'
        )

        self.xmin_label.place(x=5, y=10)
        self.xmax_label.place(x=125, y=10)

        self.xmin = Entry(
            self.window,
            style="XminMaxInput.TEntry",
            validate="key",
            validatecommand=self.vcmd
        )
        self.xmax = Entry(
            self.window,
            style="XminMaxInput.TEntry",
            validate="key",
            validatecommand=self.vcmd
        )

        self.xmin.place(x=10, y=30, width=100, height=20)
        self.xmax.place(x=130, y=30, width=100, height=20)

        # X, y coords modes and labels
        self.x_coords_mode = Combobox(
            self.window,
            values=['Auto', 'Show', 'Disable'],
            state='readonly'
        )
        self.y_coords_mode = Combobox(
            self.window,
            values=['Auto', 'Show', 'Disable'],
            state='readonly'
        )

        # Set current item for comboboxes
        self.x_coords_mode.current(0)
        self.y_coords_mode.current(0)

        self.x_coords_mode.place(x=10, y=75, width=100, height=20)
        self.y_coords_mode.place(x=130, y=75, width=100, height=20)

        self.x_coords_mode_label = Label(self.window, text='Each x coords', style="Label.TLabel")
        self.y_coords_mode_label = Label(self.window, text='Each y coords', style="Label.TLabel")

        self.x_coords_mode_label.place(x=5, y=54)
        self.y_coords_mode_label.place(x=125, y=54)

        # Only whole numbers or non-whole
        self.show_only_whole_numbers = BooleanVar()
        self.whole_numbers_checkbox = Checkbutton(
            self.window,
            variable=self.show_only_whole_numbers,
            onvalue=True,
            offvalue=False
        )
        self.whole_numbers_checkbox.place(x=10, y=100, width=20, height=20)

        self.whole_numbers_checkbox_label = Label(self.window, text='Show only whole numbers')
        self.whole_numbers_checkbox_label.place(x=30, y=100)

        # Show points on the graph line or disable
        self.points_view_variable = BooleanVar()
        self.points_view = Checkbutton(
            self.window,
            variable=self.points_view_variable,
            onvalue=True,
            offvalue=False
        )
        self.points_view.select()
        self.points_view.place(x=10, y=120, width=20, height=20)

        self.points_view_label = Label(self.window, text='Show points on the graph line')
        self.points_view_label.place(x=30, y=120)

        # Input for formulas
        self.input_for_formula_label = Label(self.window, text='Formula', style="Label.TLabel")
        self.input_for_formula_label.place(x=5, y=140)

        self.input_for_formula = Text(self.window, font=("Segoe UI", 10))
        self.input_for_formula.place(x=10, y=160, width=220, height=100)

        # Draw and clear buttons
        self.draw_btn = Button(
            self.window,
            text='Draw',
            command=self.draw_and_show_graph
        )
        self.draw_btn.place(x=10, y=450, width=220, height=40)

        self.clear_btn = Button(self.window, text='Clear', command=self.clear)
        self.clear_btn.place(x=10, y=400, width=220, height=40)

    def draw_and_show_graph(self):
        xmin_value = self.xmin.get()
        xmax_value = self.xmax.get()
        if not xmin_value:
            messagebox.showerror(
                title='Error in input',
                message="You didn't write x min"
            )
            return

        if not xmax_value:
            messagebox.showerror(
                title='Error in input',
                message="You didn't write x max"
            )
            return

        try:
            xmin_value = int(xmin_value)
        except ValueError:
            messagebox.showerror(
                title='Error in input',
                message="You write not a number in x min input"
            )
            return

        try:
            xmax_value = int(xmax_value)
        except ValueError:
            messagebox.showerror(
                title='Error in input',
                message="You write not a number in x min input"
            )
            return

        try:
            self.canvas = Canvas(root, width=640, height=480)
            self.canvas.place(x=240, y=10)
            draw_graph(
                text=self.input_for_formula.get("1.0", "end"),
                x_coords_mode=self.x_coords_mode.get().lower(),
                y_coords_mode=self.y_coords_mode.get().lower(),
                xmin=xmin_value,
                xmax=xmax_value,
                show_only_whole_numbers=self.show_only_whole_numbers.get(),
                show_points=self.points_view_variable.get()
            )
        except CalculationException:
            messagebox.showerror(
                title='Error in calculation',
                message='You wrote wrong formula'
            )
        except SyntaxException:
            messagebox.showerror(
                title='Wrong syntax',
                message='You wrote wrong formula syntax'
            )
        else:
            # Create image in window
            img = ImageTk.PhotoImage(Image.open("graph.png"))
            self.canvas.create_image(0, 0, anchor='nw', image=img)
            self.canvas.image = img

    def clear(self):
        self.xmin.delete(0, "end")
        self.xmax.delete(0, "end")
        self.input_for_formula.delete("1.0", "end")
        self.canvas.image = None


if __name__ == "__main__":
    root = Tk()
    ui = App(root)
    root.mainloop()
