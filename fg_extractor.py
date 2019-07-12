#! /usr/bin/python3
import cv2
import numpy as np

class ForegroundExtraction:
    """
    Class Foreground Subtractor
    """
    def run(self, video_path):
        """
        Run Foreground Extraction
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise Exception("Unable to open {}".format(video_path))

        # prepare
        subtractor = cv2.createBackgroundSubtractorMOG2(history=70, varThreshold=10)

        # Skip
        # cap.set(cv2.CAP_PROP_POS_FRAMES, 60)

        # process each frame
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        for _ in range(total_frames):

            ret, frame = cap.read()
            if ret == 0:
                break

            # prepare visualizer frame
            frame_vis = frame.copy()

            # Preprocess frame
            blur = cv2.GaussianBlur(frame, (13, 13), 0)

            # Extract Foreground/Background mask
            fgmask = subtractor.apply(blur)
            bgmask = subtractor.getBackgroundImage()

            # Refine Foreground mask
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel, 2)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_ERODE, kernel)

            # find edges
            edges = cv2.Canny(fgmask, 100, 200)

            # find outer boundaries
            _, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(fgmask, contours, -1, 255, -1)

            # prepare result
            result = frame.copy()
            result[fgmask == 0] = [0, 0, 0]

            # visualize
            cv2.imshow("fgmask", fgmask)
            cv2.imshow("bgmask", bgmask)
            cv2.imshow("result", result)


            # wait
            key = cv2.waitKey(100)
            if key == 27:
                break


## main function
if __name__ == "__main__":
    import os
    import argparse

    # read args
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", help="video file", type=str, required=True)
    parser.add_argument("--fps", help="fps", type=int, default=30)
    parser.add_argument("--display_resolution", help="display resolution (WxH)", type=int, nargs="+", default=[320, 240])
    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        raise Exception("Unable to locate {}".format(args.video_path))

    fg_extractor = ForegroundExtraction()

    fg_extractor.run(args.video_path)