#!/usr/bin/python

import tkinter as tk
from tkinter import filedialog
import methods as meth


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.master.minsize(200,300)

    def create_widgets(self):
        self.select = tk.Button(self)
        self.select["text"] = "Select File"
        self.select["command"] = self.get_file
        self.select.pack(side="top")

        self.v = tk.StringVar()

        self.entry = tk.Entry(self,textvariable=self.v)
        self.entry.pack(side="top")

        self.make_graph = tk.Button(self)
        self.make_graph["text"] = "Make Graph"
        self.make_graph["command"] = self.process_file
        self.make_graph.pack(side="bottom")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")


    def get_file(self):
        #self.master.minsize(400,400)
        input_file = filedialog.askopenfilename()
        self.v.set(input_file)
        print(input_file)
        self.entry["text"] = input_file
        self.entry.config(text=input_file)
        self.pack()

    def process_file(self):
        print ("intput file", self.v.get())
        code = meth.get_code_from_file(self.v.get())
        graph = meth.create_function_graph(code)
        meth.render_output(graph)


root = tk.Tk()
app = Application(master=root)
app.mainloop()