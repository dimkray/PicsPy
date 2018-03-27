#!/usr/bin/python
# -*- coding: utf-8 -*-
 
from tkinter import *
from tkinter.filedialog import *
import GetPics
import Compare
import os
 
class Form(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, background="white")   
        self.parent = parent
        self.initUI()
    
    def initUI(self):
        self.parent.title("PicsPy 0.1 - Сравнение изображений (by DimKray)")
        self.pack(fill=BOTH, expand=2)

def SetDir(event):
    global dst
    dst = askdirectory()
    dst = dst.replace('/','\\')
    print(dst)
    if dst != '':
        dir = []
        for root, files, dirs in os.walk(dst):
            dir.append(root)
        GetPics.Process(dir)
        Compare.Process()

def main():
    root = Tk() # создание диалога
    root.geometry("450x110+300+300")
    start = Label(root, text="Выберите папку для загрузки и анализа изображений:", font="Arial 8")
    start.pack()
    btn = Button(root, text="Выбрать папку изображений", width=30, height=2, bg="white", fg="black")
    btn.bind("<Button-1>", SetDir)
    btn.pack()
    auto = Label(root, text="Автоудаление изображений до указанного % похожести:", font="Arial 8")
    auto.pack()
    ent = Entry(root, width=10, bd=3, text='7')
    ent.pack()
    app = Form(root)
    root.mainloop()  
 
if __name__ == '__main__':
    main()
