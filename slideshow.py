#! /home/rusty/env/bin/python

import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, ImageOps
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
    def __init__(self, directory, sleep, master, verbose):
        super().__init__(master)

        self.directory = directory
        self.seconds = sleep
        self.master = master
        self.verbose = verbose

        self.timer = None

        self.pack()
        self.configure(bg = 'black')

        self.screen_width = self.master.winfo_screenwidth()
        self.screen_height = self.master.winfo_screenheight()

        logging.info("{}, {}".format(self.screen_width, self.screen_height))

        # - 2 to show any errant borders
        self.basewidth = self.screen_width - 2
        self.baseheight = self.screen_height - 2

        self.counter = 0
        self.repeat = 0

        self.img_id = None
        self.tk_img = None

        self.master.bind('Q', self.quit)
        self.master.bind('<Up>', self.up_key)
        self.master.bind('<Down>', self.down_key)
        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)

        self.canvas = Canvas(self, highlightthickness = 0)

        self.images = self.get_images(self.directory)

        random.shuffle(self.images)

        self.update()

        return

    ###########################################

    def get_images(self, directory):
        files = DirTree().files(directory)
        
        if len(files) == 0:
            sys.exit("nothing to display")
            
        return files

    def quit(self, event):
         logging.info("exiting")
         self.master.destroy()

         return

    ###########################################

    def up_key(self, event):
        logging.info("up pressed")
        self.seconds += 5

        return

    ###########################################

    def down_key(self, event):
        logging.info("down pressed")

        self.seconds -= 5

        if self.seconds <= 0:
            self.seconds = 1

        return

    ###########################################

    def left_key(self, event):
        logging.info("left pressed")

        self.counter -= 2

        if self.counter < 0:
            self.counter = 0
 
        self.after_cancel(self.timer)
        self.update()

        return

    ###########################################

    def right_key(self, event):
        logging.info("right pressed")

        self.after_cancel(self.timer)
        self.update()

        return

    ###########################################

    def update(self):
        self.timer = self.after(self.seconds * 1000, lambda: self.update())

        self.main()

        self.counter += 1

        if self.counter >= len(self.images):
            # re-read in case files were added or removed
            self.images = self.get_images(self.directory)
            random.shuffle(self.images)
            self.counter = 0
 
        return

    ###########################################

    def is_gif(self, image_name):
        if (image_name.endswith(".gif")):
            return(True)

        return(False)

    ###########################################

    def display_gif(self, image):
        if self.timer != None:
            self.after_cancel(self.timer)

        try:
            self.delay = int(image.info['duration'] / 2)
        except:
            print("no duration, using 50")
            self.delay = 50

        self.loc = 0

        self.display_frames(image)

        return

    ###########################################

    def display_frames(self, image):
        try:
            image.seek(self.loc)
            frame = image.copy()
        except:
            self.update()

            return

        self.display(frame)

        self.loc += 1

        self.timer = self.after(self.delay, lambda: self.display_frames(image))

        return

    ###########################################

    def resize_image(self, image):
        (img_width, img_height) = image.size
        logging.info("orig {}/{}".format(img_width, img_height))

        ratio = min(self.basewidth / img_width, self.baseheight / img_height)
        logging.info("ratio: {}".format(ratio))

        wsize = int(img_width * ratio)
        hsize = int(img_height * ratio)

        logging.info("new size: {}/{}".format(wsize, hsize))

        try:
            new_img = ImageOps.scale(image, ratio)
        except:
            logging.warning("exception in ImageOps.scale: {}".format(sys.exc_info()[0]))

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

        # delete previous image
        self.canvas.delete(self.img_id)

        self.canvas.configure(width = img_width, height = img_height, highlightthickness = 0)
        self.img_id = self.canvas.create_image(0, 0, image = self.tk_img, anchor = 'nw')
        self.canvas.pack(padx = x_pad, pady = y_pad)

        return

    ###########################################

    def main(self):
        image_name = self.images[self.counter]

        if verbose:
            print(image_name)

        logging.info("file: {}".format(image_name))

        try:
            base_img = ImageTk.Image.open(image_name)
        except:
            logging.warning("exception in Image.open: {}, {}".format(sys.exc_info()[0], image_name))

            return

        if self.is_gif(image_name):
            self.display_gif(base_img)

            return

        self.display(base_img)

        return

###########################################

def tracefunc(frame, event, arg, indent=[0]):
    if event == "call":
        indent[0] += 2
        print("-" * indent[0] + "> call function", frame.f_code.co_name)
    elif event == "return":
        print("<" + "-" * indent[0], "exit function", frame.f_code.co_name)
        indent[0] -= 2
        return tracefunc

###########################################

#logging.basicConfig(filename = '/tmp/slideshow.log', level=logging.WARNING)
logging.basicConfig(level=logging.WARNING)

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

parser.add_argument('--verbose',
                    nargs = '?',
                    help = 'display file name',
                    type = bool,
                    const = True,
                    default = False)

args = parser.parse_args()

directory = args.directory
sleep = args.sleep
verbose = args.verbose

root = tk.Tk()
app = SlideShow(directory = directory, sleep = sleep, master = root, verbose = verbose)

# sys.setprofile(tracefunc)

app.mainloop()
