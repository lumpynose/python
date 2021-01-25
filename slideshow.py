#! /home/rusty/env/bin/python

import tkinter as tk
from tkinter import Canvas
from PIL import ImageTk, ImageOps
import PIL as pil
from dirtree import DirTree
from datetime import datetime
import random
import sys
import argparse
import logging
import time
import inspect

class SlideShow(tk.Frame):
    """Display a full screen slide show.

    Q key quits, up key adds 5 seconds to the delay,
    down key subtracts 5 seconds from the delay,
    left key goes back one,
    right key goes forward one.
    """

    def __init__(self, directory, sleep, root, verbose):
        super().__init__(root)

        self.directory = directory
        self.seconds = sleep
        self.root = root
        self.verbose = verbose

        self.timer_outer = None
        self.timer_gif = None

        self.pack()
        self.configure(bg = 'black')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        logging.info("{}, {}".format(screen_width, screen_height))

        # - 2 to show any errant borders
        self.basewidth = screen_width - 2
        self.baseheight = screen_height - 2

        self.counter = 0
        self.repeat = 0
        self.end_time = 0

        self.img_id = None
        self.tk_img = None

        self.root.bind('Q', self.quitss)
        self.root.bind('<Up>', self.up_key)
        self.root.bind('<Down>', self.down_key)
        self.root.bind('<Left>', self.left_key)
        self.root.bind('<Right>', self.right_key)

        self.add_menu(self.root)

        self.canvas = Canvas(self, highlightthickness = 0)

        # self.files = self.get_files(self.directory)
        # random.shuffle(self.files)
        self.files = []

        return

    ###########################################

    def get_files(self, directory):
        #print(inspect.currentframe().f_code.co_name)
        files = DirTree().files(directory)
        
        if len(files) == 0:
            sys.exit("nothing to display")
            
        return files

    ###########################################

    def quitss(self, event = None):
        logging.info("exiting")
        self.root.destroy()

        return

    ###########################################

    def up_key(self, event = None):
        logging.info("up pressed")
        self.seconds += 5

        return

    ###########################################

    def down_key(self, event = None):
        logging.info("down pressed")

        self.seconds -= 5

        if self.seconds <= 0:
            self.seconds = 1

        return

    ###########################################

    def left_key(self, event = None):
        logging.info("left pressed")

        self.counter -= 2

        if self.counter < 0:
            self.counter = 0
 
        if self.timer_outer != None:
            self.root.after_cancel(self.timer_outer)
            self.timer_outer = None

        self.update()

        return

    ###########################################

    def right_key(self, event = None):
        logging.info("right pressed")

        if self.timer_outer != None:
            self.root.after_cancel(self.timer_outer)
            self.timer_outer = None

        self.counter += 1

        self.update()

        return

    ###########################################

    def add_menu(self, root):
        root.option_add('*tearOff', False)

        menu = tk.Menu(root)

        menu.add_command(label = 'Previous', command = self.left_key);
        menu.add_command(label = 'Next', command = self.right_key);
        menu.add_command(label = 'Quit', command = self.quitss);

        root.bind('<3>', lambda e: menu.post(e.x_root, e.y_root))

        return

    ###########################################

    def resize_image(self, image):
        #print(inspect.currentframe().f_code.co_name)
        (img_width, img_height) = image.size
        logging.info("orig {}/{}".format(img_width, img_height))

        if (img_width < self.basewidth) and (img_height < self.baseheight):
            ratio = 1
        else:
            ratio = min(self.basewidth / img_width, self.baseheight / img_height)
            logging.info("ratio: {}".format(ratio))

            wsize = int(img_width * ratio)
            hsize = int(img_height * ratio)

            logging.info("new size: {}/{}".format(wsize, hsize))

        try:
            new_img = ImageOps.scale(image, ratio)
        except:
            logging.warning("exception in ImageOps.scale: {}".format(sys.exc_info()[0]))

        image.close()

        return(new_img)

    ###########################################

    def is_gif(self, image_name):
        #print(inspect.currentframe().f_code.co_name)
        if (image_name.endswith(".gif")):
            return(True)

        return(False)

    ###########################################

    def update(self):
        print(inspect.currentframe().f_code.co_name)
        if self.counter >= len(self.files):
            # re-read in case files were added or removed
            self.files = self.get_files(self.directory)
            random.shuffle(self.files)
            self.counter = 0
 
        self.display_file()

        self.counter += 1

        #if self.counter == 2:
        #    self.root.destroy()

        self.timer_outer = self.root.after(self.seconds * 1000, lambda: self.update())

        return

    ###########################################

    # This used to do more, unrolling the frames and storing
    # them in an array which display_gif_frames() displayed.  Now
    # display_gif_frames() fetches the individual frames and displays
    # them.
    def display_gif(self, image):
        print(inspect.currentframe().f_code.co_name)
        #if self.timer_outer != None:
        #    self.root.after_cancel(self.timer_outer)
        #    self.timer_outer = None

        try:
            self.delay = int(image.info['duration'] / 4)
        except:
            logging.info("no duration, using 50")

            if self.verbose:
                print("no duration, using 50", flush = True)

            self.delay = 50

        self.frame_num = 0
        self.repeat = 0

        self.end_time = time.time() + self.seconds

        self.display_gif_frames(image)

        return

    ###########################################

    def display_gif_frames(self, image):
        print(inspect.currentframe().f_code.co_name)
        if self.timer_outer != None:
            self.root.after_cancel(self.timer_outer)
            self.timer_outer = None

        try:
            image.seek(self.frame_num)
            frame = image.copy()
        except:
            now = time.time()

            if now > self.end_time:
                logging.info("frames: {}, delay: {}, repeats: {}"
                             .format(self.frame_num - 1, self.delay, self.repeat))

                if self.verbose:
                    print("{}, {}, {}"
                          .format((self.frame_num - 1) * self.delay,
                                  self.repeat,
                                  datetime.today().ctime()),
                          flush = True)

                image.close()

                self.update()

                return

            self.repeat += 1;

            self.frame_num = 0;
            self.timer_gif = self.root.after(self.delay, lambda: self.display_gif_frames(image))

            return

        self.display_image(frame)

        frame.close()

        self.frame_num += 1

        self.timer_gif = self.root.after(self.delay, lambda: self.display_gif_frames(image))

        return

    ###########################################

    def display_image(self, image):
        print(inspect.currentframe().f_code.co_name)
        new_img = self.resize_image(image)
        
        (img_width, img_height) = new_img.size

        (x_pad, y_pad) = 0, 0

        if img_height < self.baseheight:
            y_pad = (self.baseheight - img_height) / 2

        if img_width < self.basewidth:
            x_pad = (self.basewidth - img_width) / 2

        logging.info("pading: {}/{}".format(x_pad, y_pad))

        # need to store tk_img outside or it gets garbage collected?

        try:
            self.tk_img = ImageTk.PhotoImage(new_img)
        except:
            logging.warning("exception in ImageTk.PhotoImage: {}".format(sys.exc_info()[0]))

        new_img.close()
        
        # delete previous image from canvas.create_image()
        self.canvas.delete(self.img_id)

        self.canvas.configure(width = img_width, height = img_height, highlightthickness = 0)
        self.img_id = self.canvas.create_image(0, 0, image = self.tk_img, anchor = 'nw')
        self.canvas.pack(padx = x_pad, pady = y_pad)

        return

    ###########################################

    def display_file(self):
        print(inspect.currentframe().f_code.co_name)
        file_name = self.files[self.counter]

        logging.info("file: {}".format(file_name))

        try:
            base_img = ImageTk.Image.open(file_name)
        except:
            logging.warning("exception in Image.open: {}, {}".format(sys.exc_info()[0], file_name))

            return

        if self.is_gif(file_name):
            self.display_gif(base_img)

            return

        self.display_image(base_img)

        base_img.close()

        return

###########################################

#logging.basicConfig(filename = '/tmp/slideshow.log', level=logging.WARNING)
logging.basicConfig(level = logging.WARNING)

parser = argparse.ArgumentParser(description = 'Display some images.')

parser.add_argument('--sleep',
                    help = 'How long to pause between images',
                    type = int,
                    default = 15)

parser.add_argument('--verbose',
                    help = 'display stuff',
                    action = 'store_const',
                    const = True,
                    default = False)

parser.add_argument('directory',
                    help = 'The directory of images',
                    type = str,
                    nargs = '?',
                    default = "/home/rusty/pics")

args = parser.parse_args()

directory = args.directory
sleep = args.sleep
verbose = args.verbose

if verbose:
    print(args)

root = tk.Tk()

slideshow = SlideShow(directory = directory, sleep = sleep, root = root, verbose = verbose)

# Displays the first frame and starts the timer.
slideshow.update()

root.mainloop()
