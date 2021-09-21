import cv2
from steganography.base import Stego


class Video(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video = cv2.VideoCapture(self.stego_filepath)
        self.num_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)

        while self.video.isOpened():
            ret, frame = self.video.read()
            # TODO manipulate frame
        return self.secret_bytes

    def _extract(self):
        print("extracting", self.secret_bytes[:10], "using", self.key)
        # TODO
        return self.secret_bytes
