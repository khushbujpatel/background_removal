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
    parser.add_argument("--video_path", help="video file", type=str, default="sample/video_1.mp4")
    parser.add_argument("--fps", help="frame rate", type=int, default=30)
    parser.add_argument("--display_resolution", help="display resolution (WxH)", type=int, nargs=2, default=[320, 240])
    parser.add_argument("--monochrome", help="use monochrome frames", action="store_true", default=False)
    parser.add_argument("--debug_visualize", help="enable debug windows to view masks", action="store_true", default=False)
    parser.add_argument("--target_path", help="resultant video dump target path", type=str, default=None)
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    logging.info("Display Properties: [fps: {}, display_resolution: {}x{}, monochrome: {}]".format(
        args.fps, args.display_resolution[0], args.display_resolution[1], args.monochrome))

    if not os.path.exists(args.video_path):
        raise Exception("Unable to locate {}".format(args.video_path))

    if not args.target_path:
        target_path = args.video_path.split(".")[0] + "_processed.mp4"
    else:
        target_path = args.target_path

    # Open Video Writer
    writer = cv2.VideoWriter()
    writer.open(target_path, cv2.VideoWriter_fourcc(*'XVID'), int(args.fps), tuple(args.display_resolution), isColor=not args.monochrome)
    if not writer.isOpened():
        raise Exception("Unable to open {}".format(target_path))

    # Open Video Reader
    cap = cv2.VideoCapture(args.video_path)
    if not cap.isOpened():
        raise Exception("Unable to open {}".format(args.video_path))

    cap.set(cv2.CAP_PROP_FPS, args.fps)

    fg_extractor = ForegroundExtraction()
    back_flag = False
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    for i in range(total_frames):

        ret, image = cap.read()
        if ret == 0:
            break

        if args.monochrome:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        fg = fg_extractor.extract(image, args.debug_visualize)

        # write to file
        writer.write(fg)

        # visualize
        fg = cv2.resize(fg, tuple(args.display_resolution))
        cv2.imshow("foreground", fg)
        cv2.imshow("input", image)

        # wait
        if back_flag == True:
            cv2.waitKey(0)
            back_flag = False
        key = cv2.waitKey(100)
        if key == 27:
            break
        if key == ord('p'):
            cv2.waitKey(0)
        if key == ord('b'):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i - 10)
            cv2.waitKey(0)
            back_flag = True

    writer.release()
    cap.release()
    cv2.destroyAllWindows()
