import sys
import threading
import time

import cv2
from flask import Flask, Response, render_template

from camera import VideoCamera
from email_utils import send_alert_email_to_user

email_update_interval = 10 * 60
video_camera = VideoCamera(flip=True)
body_detection_classifier = cv2.CascadeClassifier(
    "models/upperbody_recognition_model.xml"
)

app = Flask(__name__)

email_update_time = time.time()


def perform_body_detection():
    global email_update_time

    while True:
        try:
            if is_motion_detected():
                frame, found_objs_in_frame = video_camera.get_object_in_frame(
                    body_detection_classifier
                )
                if (
                    found_objs_in_frame
                    and (time.time() - email_update_time) > email_update_interval
                ):
                    email_update_time = time.time()
                    send_alert_email_to_user(frame)
        except:
            print("Error sending email: ", sys.exc_info()[0])


def is_motion_detected():
    # Implementation TBD since it may not be a required step in the detection process,
    # due to the body detection performance. Design plan was to compare frames in this step,
    # but body detectino cascade classifier seems to be sufficient to not get that many false positives

    return True


@app.route("/")
def index_page():
    return render_template("index.html")


def generate_image(camera):
    while True:
        frame, _ = camera.get_object_in_frame(body_detection_classifier)
        yield (b"--frame\r\n" b"Content-Type: image/jpeg\r\n\r\n" + frame + b"\r\n\r\n")


@app.route("/video_feed")
def video_feed_page():
    return Response(
        generate_image(video_camera),
        mimetype="multipart/x-mixed-replace; boundary=frame",
    )


if __name__ == "__main__":
    # Start a background thread to monitor the front door area, and email the user when there is a body/bodies detected
    background_thread = threading.Thread(target=perform_body_detection, args=())
    background_thread.daemon = True
    background_thread.start()

    app.run(host="0.0.0.0", debug=False)
