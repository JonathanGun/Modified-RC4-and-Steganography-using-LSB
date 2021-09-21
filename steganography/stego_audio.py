import wave
from steganography.base import Stego


class Audio(Stego):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.audio = wave.open(self.stego_filepath, "rb")

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)
        # TODO
        return wave.open(self.stego_filepath, "rb")

    def _extract(self):
        print("extracting", self.secret_bytes[:10], "using", self.key)
        # TODO
        return wave.open(self.stego_filepath, "rb")
