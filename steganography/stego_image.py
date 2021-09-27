import cv2
import numpy as np
from steganography.base import Stego


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
        secret_bytes = self._extract_lsb(list(self.image.flatten()))
        self._extract_meta_bytes(secret_bytes)
        return secret_bytes[self.secret_header_size:]
