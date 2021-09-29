import cv2
import numpy as np
from steganography.base import Stego


class Video(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.video = cv2.VideoCapture(self.stego_filepath)
        self.num_frames = self.video.get(cv2.CAP_PROP_FRAME_COUNT)
        self.fps = self.video.get(cv2.CAP_PROP_FPS)
        frameCount = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))
        frameWidth = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH))
        frameHeight = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.video_shape = (frameCount, frameHeight, frameWidth, 3)
        size = f"{frameCount * frameHeight * frameWidth * 3 / 1024 / 1024} MiB"
        print(self.video_shape, size)
        if frameCount * frameHeight * frameWidth * 3 > 100_000_000:
            raise ValueError("file too big:", size)
        self.video_frames = np.empty(self.video_shape, np.dtype('uint8'))
        fc = 0
        ret = True
        while fc < frameCount and ret:
            ret, self.video_frames[fc] = self.video.read()
            fc += 1

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)
        return np.ndarray(
            buffer=np.array(self._insert_lsb(
                stego_bytes=list(self.video_frames.flatten()),
                secret_bytes=self.secret_bytes,
            ), dtype="uint8"),
            shape=self.video_shape,
            dtype="uint8",
        )

    def _extract(self):
        print("extracting", self.secret_bytes[:10], "using", self.key)
        return self._extract_lsb(list(self.video_frames.flatten()))
