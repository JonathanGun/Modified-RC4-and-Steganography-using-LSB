import cv2
import numpy as np
from steganography.base import Stego
import math


class Image(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = cv2.imread(self.stego_filepath)

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)
        return np.ndarray(
            buffer=np.array(self._insert_lsb(
                stego_bytes=list(self.image.flatten()),
                secret_bytes=self.secret_bytes,
            ), dtype="uint8"),
            shape=self.image.shape,
            dtype="uint8",
        )

    def _extract(self):
        print("extracting", self.image[0][:10], "using", self.key)
        return self._extract_lsb(list(self.image.flatten()))

    def calculate_psnr(self, original_img, stego_img):
        val = np.sum(pow(original_img - stego_img, 2)) / (original_img.shape[0] * original_img.shape[1])
        rms = math.sqrt(val)
        psnr = 20 * math.log10(255 / rms)
        return round(psnr, 1)
