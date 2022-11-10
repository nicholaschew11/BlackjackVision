import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera

from threading import Thread

class Video:
    def __init__(self, resolution = (640, 480), framerate = 30):
        # PiCamera and image stream initialization
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera,size = resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture, format = "bgr", use_video_port = True)
        self.frame = []
        self.stopped = False

    def start(self):
	# Frame reading thread start
        Thread(target = self.refresh, args = ()).start()
        return self

    def refresh(self):
        # Refresh until thread ended
        for f in self.stream:
            # Grab the frame from the stream and clear the stream
            self.frame = f.array
            self.rawCapture.truncate(0)
            if self.stopped:
                self.stream.close()
                self.rawCapture.close()
                self.camera.close()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
