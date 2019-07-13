#! /usr/bin/python3

# import the necessary packages
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2

from fg_extractor import ForegroundExtraction



class Application:

    def __init__(self, video_path, fps=30):
        self.frame_id = 0
        self.root = Tk()

        self.prev_button = Button(self.root, text="Previous", command=self.prev_frame)
        self.pause_button = Button(self.root, text="Pause", command=self.pause_frame)
        self.play_button = Button(self.root, text="Play", command=self.play_frame)

        self.prev_button.pack(side="bottom")
        self.pause_button.pack(side="bottom")
        self.play_button.pack(side="bottom")

        self.panel = None

        self.fps = fps
        self.pause = False

        # Open Video Reader
        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            raise Exception("Unable to open {}".format(video_path))

        self.fg_extractor = ForegroundExtraction()

        if self.pause:
            self.video_loop()

    def prev_frame(self):
        self.frame_id -= 2
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.frame_id)
        self.video_loop()

    def pause_frame(self):
        self.pause = True
        self.video_loop()

    def play_frame(self):
        self.pause = False
        self.video_loop()

    def video_loop(self):
        ret, image = self.cap.read()
        if ret:
            # extract foreground
            fg = self.fg_extractor.extract(image)

            # write frame number
            cv2.putText(fg, "frame {}".format(self.frame_id), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 255, 100), 1, cv2.LINE_AA)

            # load in gui
            tkimage = cv2.cvtColor(fg, cv2.COLOR_BGR2RGB)
            tkimage = Image.fromarray(tkimage)
            tkimage = ImageTk.PhotoImage(tkimage)

            # init panel
            if self.panel is None:
                self.panel = Label(image=tkimage)
                self.panel.image = tkimage
                self.panel.pack(side="left", padx=10, pady=10)

            # otherwise, simply update the panel
            else:
                self.panel.configure(image=tkimage)
                self.panel.image = tkimage

            self.frame_id += 1

            if not self.pause:
                self.root.after(self.fps, self.video_loop)

    def launch(self):
        self.root.mainloop()

    def __del__(self):
        self.cap.release()
        self.root.quit()


if __name__ == "__main__":
    app = Application("sample/video_1.mp4")
    app.launch()
