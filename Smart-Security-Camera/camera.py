import time

import cv2
import numpy as np
from imutils.video.pivideostream import PiVideoStream

CLASSIFIER_MIN_NEIGHBORS = 5
CLASSIFIER_MIN_OBJECT_SIZE = 30
CLASSIFIER_IMAGE_SCALE_FACTOR = 1.1

BOUNDING_BOX_COLOR = (0, 255, 0)
BOUNDING_BOX_THICKNESS = 2


class VideoCamera(object):
    def __init__(self, flip_image=False):
        self.vs = PiVideoStream().start()
        self.flip_image = flip_image
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_image_if_needed(self, frame):
        if self.flip_image:
            return np.flip(frame, 0)

        return frame

    def get_camera_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        _, jpeg_frame = cv2.imencode(".jpg", frame)

        return jpeg_frame.tobytes()

    def get_object_in_frame(self, classifier):
        found_objects_in_frame = False

        # Flip the frame if needed (the camera is mounted upside-down on the door)
        frame = self.flip_if_needed(self.vs.read()).copy()

        # Convert image to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        objects = classifier.detectMultiScale(
            gray,
            minNeighbors=CLASSIFIER_MIN_NEIGHBORS,
            minSize=(CLASSIFIER_MIN_OBJECT_SIZE, CLASSIFIER_MIN_OBJECT_SIZE),
            scaleFactor=CLASSIFIER_IMAGE_SCALE_FACTOR,
            flags=cv2.CASCADE_SCALE_IMAGE,
        )

        if len(objects) > 0:
            found_objects_in_frame = True

        # Draw a bounding box around the objects
        for (x, y, w, h) in objects:
            start_point = (x, y)
            end_point = (x + w, y + h)

            cv2.rectangle(
                frame,
                start_point,
                end_point,
                BOUNDING_BOX_COLOR,
                BOUNDING_BOX_THICKNESS,
            )

        _, jpeg_frame = cv2.imencode(".jpg", frame)

        return (jpeg_frame.tobytes(), found_objects_in_frame)
