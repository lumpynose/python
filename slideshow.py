#! /home/rusty/env/bin/python

import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk
import PIL as pil
from dirtree import DirTree
import random
import sys
import argparse
import logging

# display a full screen slide show.
# Q key quits, up key adds 5 seconds to the delay,
# down key subtracts 5 seconds from the delay,
# left key goes back one,
# right key goes forward one.
class SlideShow(tk.Frame):
    def __init__(self, files, sleep, master):
        super().__init__(master)

        self.images = files
        self.seconds = sleep
        self.master = master
        self.timer = None;

        self.pack()
        self.configure(bg = 'black')

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        logging.info("{}, {}".format(self.screen_width, self.screen_height)
        )
        
        # - 2 to show any errant borders
        self.basewidth = self.screen_width - 2
        self.baseheight = self.screen_height - 2

        self.counter = 0
        self.img_id = None

        self.master.bind('Q', self.quit)
        self.master.bind('<Up>', self.up_key);
        self.master.bind('<Down>', self.down_key)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)

        self.canvas = Canvas(self, highlightthickness = 0)

        random.shuffle(self.images)

        self.update()

        return

    ###########################################

    def update(self):
        self.main()

        self.counter += 1

        if self.counter >= len(self.images):
            random.shuffle(self.images)
            self.counter = 0

        self.timer = self.master.after(self.seconds * 1000, self.update)

        return

    ###########################################

    def quit(self, event):
         logging.info("exiting")
         self.master.destroy()

         return

    ###########################################

    def up_key(self, event):
        logging.info("up pressed")
        self.seconds += 5;

        return

    ###########################################

    def down_key(self, event):
        logging.info("down pressed")

        if (self.seconds - 5) <= 0:
            self.seconds = 1
        else:
            self.seconds -= 5

        return

    ###########################################

    def left_key(self, event):
        logging.info("left pressed")

        if (self.counter - 2) < 0:
            self.counter = 0
        else:
            self.counter -= 2

        self.master.after_cancel(self.timer)
        self.update()

        return

    ###########################################

    def right_key(self, event):
        logging.info("right pressed")

        self.master.after_cancel(self.timer)
        self.update()

        return

    ###########################################

    def is_gif(self, image_name):
        if (image_name.endswith(".gif")):
            logging.info("is gif: {}".format(image_name))
            print("is gif: ", image_name)
            return(True)

        return(False)

    ###########################################

    def display_gif(self, image):
        self.frames = []

        try:
            self.delay = image.info['duration']
            print("duration: ", self.delay)
        except:
            self.delay = 100

        try:
            i = 0
            while True:
                image.seek(i)
                self.frames.append(ImageTk.PhotoImage(image.copy()))
                self.frames[i].size= image.size
                print("i: ", i)
                i += 1
        except EOFError:
            print("EOFError")
            pass

        if len(self.frames) == 1:
            print("only 1 frame")
            display(image)
            return

        if (self.timer != None):
            self.master.after_cancel(self.timer)

        self.loc = 0;
        
        self.display_frame()

        return
    
    ###########################################

    def display_frame(self):
        if self.frames:
            self.display(self.frames[self.loc])

            self.loc += 1
            self.loc %= len(self.frames)

            if self.loc > 0:
                self.after(self.delay, self.display_frame)
            else:
                self.update()
                
        return

    ###########################################

    def resize_image(self, image):
        (img_width, img_height) = image.size
        logging.info("orig {}/{}".format(img_width, img_height))

        ratio = min(self.basewidth / img_width, self.baseheight / img_height)
        logging.info("ratio: {}".format(ratio))

        wsize = int(img_width * ratio);
        hsize = int(img_height * ratio);

        logging.info("new size: {}/{}".format(wsize, hsize))

        try:
            new_img = image.resize((wsize, hsize), pil.Image.ANTIALIAS)
        except:
            logging.warning("exception in image.resize: {}".format(sys.exc_info()[0]))
            # return(image)

        return(new_img)
    
    ###########################################

    def display(self, image):
        new_img = self.resize_image(image)
        
        # reload width and height with new resized values
        (img_width, img_height) = new_img.size

        if img_height < self.screen_height:
            y_pad = (self.screen_height - img_height) / 2

        if img_width < self.screen_width:
            x_pad = (self.screen_width - img_width) / 2

        logging.info("pading: {}/{}".format(x_pad, y_pad))

        try:
            self.tk_img = ImageTk.PhotoImage(new_img)
        except:
            logging.warning("exception in ImageTk.PhotoImage: {}".format(sys.exc_info()[0]))
            # return

        # delete previous image
        self.canvas.delete(self.img_id)

        self.canvas.configure(width = img_width, height = img_height, highlightthickness = 0)
        self.img_id = self.canvas.create_image(0, 0, image = self.tk_img, anchor = 'nw')
        self.canvas.pack(padx = x_pad, pady = y_pad)

        return
    
    ###########################################

    def main(self):
        image_name = self.images[self.counter]
        
        logging.info("file: {}".format(image_name))

        try:
            base_img = ImageTk.Image.open(image_name)
        except:
            logging.warning("exception in Image.open: {}, {}".format(sys.exc_info()[0], image_name))
            return
        
        print("size: ", base_img.size)

        # if self.is_gif(image_name):
        #    self.display_gif(base_img)
        #    # return

        self.display(base_img)
        
        return

###########################################
logging.basicConfig(filename = '/tmp/slideshow.log', level=logging.WARNING)

parser = argparse.ArgumentParser(description = 'Display some images.')

parser.add_argument('directory',
                    nargs = '?',
                    help = 'The directory of images',
                    default = "/home/rusty/pics")

parser.add_argument('--sleep',
                    nargs = '?',
                    help = 'How long to pause between images',
                    type = int,
                    default = 15)

args = parser.parse_args()

dir = args.directory
sleep = args.sleep

files = DirTree().files(dir)

if len(files) == 0:
    sys.exit("nothing to display")

root = tk.Tk()
app = SlideShow(files = files, sleep = sleep, master = root)
app.mainloop()
