import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, askyesno, showinfo
from tkinter.filedialog import *


class MyApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.master.title("Master Title")
        self.master.iconbitmap("sample-icon.ico")

        # Set geometry: upper-left corner of the window
        ww = 628  # width
        wh = 382  # height
        wx = (self.master.winfo_screenwidth() - ww) / 2
        wy = (self.master.winfo_screenheight() - wh) / 2
        # assign geometry
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))
        # assign space holders around widgets
        self.dx = 5
        self.dy = 5

        # Menu Bar
        self.mbar = tk.Menu(self)  # create standard menu bar
        self.master.config(menu=self.mbar)  # make self.mbar standard menu bar
        # add menu entry
        self.ddmenu = tk.Menu(self, tearoff=0)
        self.mbar.add_cascade(label="A Drop Down Menu", menu=self.ddmenu)  # attach entry it to standard menu bar
        self.ddmenu.add_command(label="Drop Down Entry 1", command=lambda: self.hello("Drop Down Menu!"))

        # Label
        self.a_label = tk.Label(master, text="A Label")
        self.a_label.grid(column=0, row=0, padx=self.dx, pady=self.dy)

        # Button
        self.a_button = tk.Button(master, text="A Button", command=lambda: self.hello("The Button!"))
        self.a_button.grid(column=0, row=1, padx=self.dx, pady=self.dy)

        # Entry
        self.an_entry = tk.Entry(master, width=20)
        self.an_entry.grid(column=0, row=2, padx=self.dx, pady=self.dy)

        # Combobox
        self.cbox = ttk.Combobox(master, width=20)
        self.cbox.grid(column=0, row=3, padx=self.dx, pady=self.dy)
        self.cbox['state'] = 'readonly'
        self.cbox['values'] = ["Combobox Entry 1", "Combobox Entry 2", "Combobox Entry ..."]
        self.cbox.set("Combobox Entry 1")
        self.cbox_selection = self.cbox.get()

        # Listbox with Scrollbar
        self.scrlbar = tk.Scrollbar(master, orient=tk.VERTICAL)
        self.scrlbar.grid(stick=tk.W, column=1, row=4, padx=self.dx, pady=self.dy)
        self.lbox = tk.Listbox(master, height=3, width=20, yscrollcommand=self.scrlbar.set)
        for e in ["Listbox Entry 1", "Listbox Entry 2", "With Scrollbar ->", "lb entry n"]:
            self.lbox.insert(tk.END, e)
        self.lbox.grid(sticky=tk.E, column=0, row=4, padx=self.dx, pady=self.dy)
        self.scrlbar.config(command=self.lbox.yview)
        self.lbox_selection = self.lbox.get(0)

        # Checkbutton
        self.check_variable = tk.BooleanVar()
        self.cbutton = tk.Checkbutton(master, text="Tick this Checkbutton", variable=self.check_variable)
        self.cbutton.grid(sticky=tk.E, column=2, row=0, padx=self.dx, pady=self.dy)

        # Image
        logo = tk.PhotoImage(file=os.path.dirname(os.path.abspath(__file__)) + "/sunny-image.gif")
        logo = logo.subsample(2, 2)  # controls size
        self.l_img = tk.Label(master, image=logo)
        self.l_img.image = logo
        self.l_img.grid(row=1, column=2, rowspan=4)
        # create a placeholder to relax layout
        tk.Label(text="                                                    ").grid(row=0, column=1)

    @staticmethod
    def hello(message):
        showinfo("Got Message from ...", message)

    def quit_gui(self):
        self.master.destroy()


if __name__ == '__main__':
    MyApp().mainloop()

