from steganography.base import Stego


class Audio(Stego):
    EXTRA_META_BYTES = 44

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.stego_out_filepath = "out"
        with open(self.stego_filepath, 'rb') as fd:
            self.audio = fd.read()

    def _hide(self):
        print("hiding", self.secret_bytes[:10], "using", self.key)
        return self._insert_lsb(
            stego_bytes=list(self.audio),
            secret_bytes=self.secret_bytes
        )

    def _extract(self):
        print("extracting", self.audio[self.EXTRA_META_BYTES:64], "using", self.key)
        return self._extract_lsb(stego_bytes=list(self.audio), audio_type=True)
