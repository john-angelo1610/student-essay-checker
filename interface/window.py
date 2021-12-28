from tkinter import *
from tkinter import filedialog
from difflib import SequenceMatcher #sequence matcher
from boyer_moore_horspool import *
import tkinter as tk
import os
import docx2txt

docs = []

def add_files():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\Admin\\Documents",
                                          title="Select document",
                                          filetypes=(("docx files", "*.docx"),
                                                    ("all files", "*.*")))
    try:
        entry1.configure(state="normal")
        file = docx2txt.process(filepath)
        print(file)
        entry1.insert(tk.END,f"{os.path.basename(filepath)} successfully added\n")
        entry1.configure(state="disabled")
        docs.append(filepath)
    except:
        entry1.configure(state="normal")
        entry1.insert(tk.END,f"{os.path.basename(filepath)} is not a .docx file \n")
        entry1.configure(state="disabled")

def check_files():
    #check = BoyerMooreHorspool(docs[0],docs[1])
    #print(check.search())
    result = (SequenceMatcher(None, docs[0], docs[1]).ratio()) * 100
    print(f"{round(result)}%")
    entry0.configure(state="normal")
    entry0.insert(tk.END, f"{os.path.basename(docs[0])} and {os.path.basename(docs[1])} is {round(result)}% similar\n")
    entry0.configure(state="disabled")
    

window = Tk()

window.geometry("933x700")
window.configure(bg = "#6abfd3")
canvas = Canvas(
    window,
    bg = "#6abfd3",
    height = 700,
    width = 933,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    643.0, 441.5,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = add_files,
    relief = "flat")

b0.place(
    x = 347, y = 523,
    width = 153,
    height = 41)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = check_files,
    relief = "flat")

b1.place(
    x = 347, y = 581,
    width = 153,
    height = 41)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    734.0, 350.0,
    image = entry0_img)

entry0 = Text(
    bd = 0,
    fg = "#fff",
    bg = "#303e48",
    highlightthickness = 0)

entry0.place(
    x = 568, y = 35,
    width = 332,
    height = 628)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    178.5, 572.5,
    image = entry1_img)

entry1 = Text(
    bd = 0,
    fg = "#fff",
    bg = "#000000",
    highlightthickness = 0)

entry1.place(
    x = 39, y = 480,
    width = 279,
    height = 183)

window.resizable(False, False)
window.mainloop()
