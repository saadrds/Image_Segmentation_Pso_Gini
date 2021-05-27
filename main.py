import string
from tkinter import *
from tkinter import filedialog
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
    lbl.place(x=60, y=60)
    return fln


root = Tk()
root.geometry("1000x1000")

frame1 = Frame(root, width=460, height=500, highlightbackground="Black", highlightthickness=5)
frame1.place(x=0, y=0)
frame2 = Frame(root, width=450, height=500, highlightbackground="Black", highlightthickness=5)
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

browserButton = Button(root, text="Browser Image", padx=30, command=showImage)
browserButton.pack(side=tk.LEFT)
browserButton.place(x=100, y=450)

exitButton = Button(root, text="Exit", padx=30, command=lambda: exit())
exitButton.pack()
exitButton.place(x=260, y=450)

labelReg = Label(root, text="")
labelReg.place(x=660, y=420)


def segmenter(i):
    global labelReg
    labelReg = Label(root, text="loading", bg="red")
    labelReg.place(x=580, y=400)
    [optimum, img_path] = psoAlgo.pso(file_path, int(entreeIter.get()), int(entreeReg.get()), progress)
    img = Image.open(img_path)
    img.thumbnail((350, 350))
    img = ImageTk.PhotoImage(img)
    lbl1.configure(image=img)
    lbl1.image = img
    lbl1.place(x=560, y=60)
    mystr = "Optimum est : [ "
    for i in range(len(optimum) - 1):
        mystr += str(optimum[i]) + ", "
    mystr += str(optimum[len(optimum) - 1]) + "]"
    labelReg = Label(root, text=mystr, bg="red")
    labelReg.place(x=560, y=400)


def background(func, args):
    th = threading.Thread(target=func, args=args)
    try:
        th.daemon = True
        th.start()
    except (KeyboardInterrupt, SystemExit):
        exit()


# Progress bar widget
progress = Progressbar(root, orient=HORIZONTAL,
                       length=190, mode='determinate')


# Function responsible for the updation
# of the progress bar value
def bar():
    import time
    progress['value'] = 20
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 40
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 50
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 60
    root.update_idletasks()
    time.sleep(1)

    progress['value'] = 80
    root.update_idletasks()
    time.sleep(1)
    progress['value'] = 100


progress.place(x=570, y=420)

runButton = Button(root, text="Segmenter", padx=30, command=lambda: background(segmenter, (progress,)))
runButton.pack()
runButton.place(x=600, y=450)
# PsoAlgo.pso(file_path, int(entreeReg.get()), int(entreeIter.get())
root.title("Segmentation des images")
root.geometry("900x500")
root.resizable(width=False, height=False)
photo = PhotoImage(file = "sources/Cameraman256.png")
root.iconphoto(False, photo)
root.configure(background='black')
root.mainloop()
