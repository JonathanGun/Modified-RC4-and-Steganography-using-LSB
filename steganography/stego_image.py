import cv2
from steganography.base import Stego


class Image(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = cv2.imread(self.stego_filepath)

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)

        # Validate enough byte on stego image to hide msg
        n_bytes = self.image.shape[0] * self.image.shape[1]
        max_secret_bytes = n_bytes - self.secret_header_size
        if len(self.secret_bytes) > max_secret_bytes:
            raise ValueError('Insufficient bytes, need bigger image / less data')

        # TODO
        n_fill = 0
        for item in self.image:
            for pixel in item:
                i = 0
                while (n_fill < len(self.secret_bytes)):
                    lsb = format(pixel[i], "08b")
                    pixel[i] = int(lsb[-1] + format(self.secret_bytes[n_fill], "08b"), 2)
                    n_fill += 1
                    i = (i+1) % 3

        return self.image

    def _extract(self):
        print("extracting", self.secret_bytes[:10], "using", self.key)
        # TODO
        return self.stego_bytes
