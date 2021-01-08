import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, Image, ImageOps
from dirtree import DirTree
import random

class Drawit(tk.Frame):
    def __init__(self, files, master):
        super().__init__(master)
        self.master = master
        self.pack()
        self.configure(bg = 'black')

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        # print(self.screen_width, self.screen_height)
        
        # - 2 to show any errant borders
        self.basewidth = self.screen_width - 2
        self.baseheight = self.screen_height - 2

        self.counter = 0

        self.master.bind('Q', self.quit)
        self.master.bind('<Up>', self.up_key);
        self.master.bind('<Down>', self.down_key)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)

        self.canvas = Canvas(self, highlightthickness = 0)

        self.images = files

        random.shuffle(self.images)

        self.seconds = 5
        
        self.update()

    ###########################################

    def update(self):
        self.main()

        self.counter = self.counter + 1

        if self.counter >= len(self.images):
            random.shuffle(self.images)
            self.counter = 0

        self.timer = self.master.after(self.seconds * 1000, self.update)

    ###########################################

    def quit(self, event):
         # print("exiting")
         self.master.destroy()

    ###########################################

    def up_key(self, event):
        # print("up pressed")
        self.seconds = self.seconds + 5;

    ###########################################

    def down_key(self, event):
        # print("down pressed")

        if (self.seconds - 5) <= 0:
            self.seconds = 1
        else:
            self.seconds = self.seconds - 5

    ###########################################

    def left_key(self, event):
        # print("left pressed")

        if (self.counter - 2) < 0:
            self.counter = 0
        else:
            self.counter = self.counter -2

        self.master.after_cancel(self.timer)
        self.update()

    ###########################################

    def right_key(self, event):
        # print("right pressed")

        self.master.after_cancel(self.timer)
        self.update()

    ###########################################

    def main(self):
        print(self.images[self.counter])
        base_img = Image.open(self.images[self.counter])

        (img_width, img_height) = base_img.size
        # print('orig ', img_width, img_height)

        ratio = min(self.basewidth / img_width, self.baseheight / img_height)
        wsize = int(img_width * ratio);
        hsize = int(img_height * ratio);
        base_img = base_img.resize((wsize, hsize), Image.ANTIALIAS)
                 
        # reload width and height with new resized values
        (img_width, img_height) = base_img.size
        # print('new ', img_width, img_height)

        if img_width > img_height:
            x_pad = 0;
            y_pad = (self.screen_height - img_height) / 2
        else:
            y_pad = 0;
            x_pad = (self.screen_width - img_width) / 2
            
        self.img = ImageTk.PhotoImage(base_img)

        self.canvas.configure(width = img_width, height = img_height, highlightthickness = 0)
        self.canvas.create_image(0, 0, image = self.img, anchor = 'nw')
        self.canvas.pack(padx = x_pad, pady = y_pad)

###########################################

dirTree = DirTree()
files = dirTree.files()
# print(len(files))

root = tk.Tk()
app = Drawit(files, master = root)
app.mainloop()

