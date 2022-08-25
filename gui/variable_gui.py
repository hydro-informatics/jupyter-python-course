import tkinter as tk
from tkinter.messagebox import showinfo
import random


class MyApp(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        self.master.title("GUI with Variables")
        self.master.iconbitmap("sample-icon.ico")

        # Set geometry: upper-left corner of the window
        ww = 628  # width
        wh = 100  # height
        wx = (self.master.winfo_screenwidth() - ww) / 2
        wy = (self.master.winfo_screenheight() - wh) / 2
        # assign geometry
        self.master.geometry("%dx%d+%d+%d" % (ww, wh, wx, wy))

        self.a_label = tk.Label(master, text="Enter a value to call:")
        self.a_label.grid(column=0, row=0, padx=5, pady=5)

        # define tk.StringVar() and assign it to an entry
        self.user_entry = tk.StringVar()
        self.an_entry = tk.Entry(master, width=20, textvariable=self.user_entry)
        self.an_entry.grid(column=1, row=0, padx=5, pady=5)

        # define Button to trigger call back
        self.a_button = tk.Button(master, text="A Button", command=lambda: self.message_distributor())
        self.a_button.grid(column=2, row=0, padx=5, pady=5)

        # define a Checkbutton to use either user input or a random message
        self.check_variable = tk.BooleanVar()
        self.cbutton = tk.Checkbutton(master, text="Check this box to use a random message instead of the entry",
                                      variable=self.check_variable)
        self.cbutton.grid(sticky=tk.E, column=0, columnspan=3, row=1, padx=5, pady=5)

    def message_distributor(self):
        if not self.check_variable.get():
            showinfo("User message", self.user_entry.get())
        else:
            showinfo("Random message", self.random_message())

    def random_message(self):
        random_words = ["summer", "winter", "is", "cold", "hot", "will be"]
        return " ".join(random.sample(random_words))


if __name__ == '__main__':
    MyApp().mainloop()

