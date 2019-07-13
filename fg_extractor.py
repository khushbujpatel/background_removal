#! /usr/bin/python3
import cv2


class ForegroundExtraction:
    """
    Class Foreground Subtractor
    """
    def __init__(self):
        self.subtractor = cv2.createBackgroundSubtractorMOG2(history=70, varThreshold=10)

    def extract(self, image, debug_visualize=False):
        """
        Run Foreground Extraction
        """
        # prepare visualizer image
        fg = image.copy()

        # Preprocess image
        blur = cv2.GaussianBlur(image, (13, 13), 0)

        # Extract Foreground/Background mask
        fgmask = self.subtractor.apply(blur)
        bgmask = self.subtractor.getBackgroundImage()

        # Refine Foreground mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_DILATE, kernel, 2)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_ERODE, kernel)

        # find edges
        edges = cv2.Canny(fgmask, 100, 200)

        # find outer boundaries
        _, contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(fgmask, contours, -1, 255, -1)

        # prepare result
        fg[fgmask == 0] = [0, 0, 0]

        # visualize
        if debug_visualize:
            cv2.imshow("fgmask", fgmask)
            cv2.imshow("bgmask", bgmask)
            cv2.imshow("input", image)

        return fg
