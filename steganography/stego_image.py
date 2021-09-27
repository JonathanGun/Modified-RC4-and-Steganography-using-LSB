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

        # convert int to binary stream
        secret_bin = "".join([format(b, "08b") for b in self.secret_bytes])
        n_fill = 0
        # hide each 1's or 0's to each pixel (r,g,b) lsb
        for item in self.image:
            for pixel in item:
                i = 0
                while (n_fill < len(secret_bin)) and i < 3:
                    pixel_bin = format(pixel[i], "08b")
                    pixel[i] = int(pixel_bin[:-1] + secret_bin[n_fill], 2)
                    n_fill += 1
                    i += 1
        # TODO if insert random, acak lsbnya setelah dihide
        return self.image

    def __extract_util(self, start, end=None):
        # extract from start-th byte to end-th byte, remember 1 byte = 8 bits
        extracted_bins = []
        n_fill = 0
        reach_end = False
        for item in self.image:
            if reach_end:
                break
            for pixel in item:
                if reach_end:
                    break
                i = 0
                while not reach_end and i < 3:
                    if n_fill >= start * 8:
                        pixel_bin = format(pixel[i], "08b")
                        extracted_bins.append(pixel_bin[-1])
                    n_fill += 1
                    i += 1
                    if end is not None and n_fill >= end * 8:
                        reach_end = True
        # group and convert bits to list of bytes (int)
        extracted_bytes = list(map(lambda x: int(x, 2), ["".join(extracted_bins[i: i + 8]) for i in range(0, len(extracted_bins), 8)]))
        return extracted_bytes

    def _extract_meta_data(self):
        meta_bytes = self.__extract_util(0, self.LEN_META_METABYTE)
        secret_filename = self.__extract_util(self.LEN_META_METABYTE, self.LEN_META_METABYTE + meta_bytes[self.LEN_SECRET_FILENAME_BYTE])
        meta_bytes.extend(secret_filename)
        return meta_bytes

    def _extract(self):
        print("extracting", self.image[0][:10], "using", self.key)
        meta_bytes = self._extract_meta_data()
        self._extract_meta_bytes(meta_bytes)
        # TODO if insert random, revert acak lsbnya sebelum diextract
        self.out_bytes = self.__extract_util(self.secret_header_size)
        return self.out_bytes
