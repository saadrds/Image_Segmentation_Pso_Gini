import string
from tkinter import *
from tkinter import filedialog, ttk
import os
import tkinter as tk
from tkinter.ttk import Progressbar
from PIL import Image, ImageTk
import psoAlgo
import threading

file_path = "1"


def showImage():
    fln = filedialog.askopenfilename(initialdir=os.getcwd(), title="select Image",
                                     filetypes=(("ALL Files", "*.*"), ("JPG File", "*.jpg"), ("PNG File", "*.png")))
    global file_path
    file_path = fln
    img = Image.open(fln)
    img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img)
    lbl.image = img
    lbl.place(x=60, y=70)
    return fln


root = Tk()
root.geometry("1000x1000")

frame1 = Frame(root, width=500, height=500, highlightbackground="Black", highlightthickness=3)
frame1.configure(background='#5a94a9')
frame1.place(x=0, y=0)
frame2 = Frame(root, width=500, height=500, highlightbackground="Black", highlightthickness=3)
frame2.configure(background='#5a94a9')
frame2.place(x=450, y=0)

# label
labelReg = Label(root, text="Entrez le nombre de regions : ", bg="yellow")
labelReg.place(x=60, y=420)
entreeReg = Entry(root, textvariable=int, width=30)
entreeReg.pack(side=tk.LEFT)
entreeReg.place(x=250, y=390)
# entrée

entreeIter = Entry(root, textvariable=int, width=30)
entreeIter.pack(side=tk.LEFT)
entreeIter.place(x=250, y=420)
labelReg = Label(root, text="Entrez le nombre d'iterations : ", bg="yellow")
labelReg.place(x=60, y=390)

lbl = Label(root)
lbl.pack()
lbl1 = Label(root)
lbl1.pack()
s = ttk.Style()
s.configure('TButton', font=('calibri', 10, 'bold', 'underline'), foreground='red')
s.map('TButton',
      background=[('disabled', '#d9d9d9'), ('active', '#ececec')],
      foreground=[('disabled', '#a3a3a3')],
      relief=[('pressed', '!disabled', 'sunken')])
browserButton = ttk.Button(root, text="Select Image", command=showImage)
browserButton.pack(side=tk.LEFT)
browserButton.place(x=290, y=28)

imagefirst = Label(root,
                   text="Image Selectionée : ").place(x=40,
                                                      y=30)

exitButton = ttk.Button(root, text="Exit", command=root.destroy)
exitButton.pack()
exitButton.place(x=190, y=450)


def segmenter(i):
    global labelOpt
    imagefirst = Label(root,
                       text=" Image segmenté  :").place(x=620,
                                                        y=30)
    [optimum, img_path] = psoAlgo.pso(file_path, int(entreeIter.get()), int(entreeReg.get()), progress)
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(img)
    lbl1.configure(image=img)
    lbl1.image = img
    lbl1.place(x=560, y=70)
    mystr = "Optimum est : [ "
    for i in range(len(optimum) - 1):
        mystr += str(optimum[i]) + ", "
    mystr += str(optimum[len(optimum) - 1]) + "]"
    labelOpt = Label(root, text=mystr, bg="red")
    labelOpt.place(x=600, y=365)


def background(func, args):
    th = threading.Thread(target=func, args=args)
    try:
        th.daemon = True
        th.start()
    except (KeyboardInterrupt, SystemExit):
        exit()


# Progress bar widget
progress = Progressbar(root, orient=HORIZONTAL,
                       length=220, mode='determinate')

progress.place(x=570, y=420)

runButton = ttk.Button(root, text="Segmenter", command=lambda: background(segmenter, (progress,)))
runButton.pack()
runButton.place(x=640, y=450)
# PsoAlgo.pso(file_path, int(entreeReg.get()), int(entreeIter.get())
root.title("Segmentation des images")
root.geometry("900x500")
root.resizable(width=False, height=False)
photo = PhotoImage(file="sources/Cameraman256.png")
root.iconphoto(False, photo)
root.mainloop()
