#! /usr/bin/python3
import argparse
import logging
import os

import cv2

from fg_extractor import ForegroundExtraction

## main function
if __name__ == "__main__":
    # read args
    parser = argparse.ArgumentParser()
    parser.add_argument("--video_path", help="video file", type=str, required=True)
    parser.add_argument("--fps", help="fps", type=int, default=30)
    parser.add_argument("--display_resolution", help="display resolution (WxH)", type=int, nargs=2, default=[320, 240])
    parser.add_argument("--debug_visualize", help="enable debug windows to view masks", action="store_true", default=False)
    args = parser.parse_args()

    if not os.path.exists(args.video_path):
        raise Exception("Unable to locate {}".format(args.video_path))

    logging.basicConfig(level=logging.INFO)

    cap = cv2.VideoCapture(args.video_path)
    if not cap.isOpened():
        raise Exception("Unable to open {}".format(args.video_path))

    fg_extractor = ForegroundExtraction()

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for _ in range(total_frames):

        ret, image = cap.read()
        if ret == 0:
            break

        fg = fg_extractor.extract(image, args.debug_visualize)

        # visualize
        cv2.imshow("foreground", fg)

        # wait
        key = cv2.waitKey(100)
        if key == 27:
            break
        if key == 32:
            cv2.waitKey(0)

    cap.release()
    cv2.destroyAllWindows()
