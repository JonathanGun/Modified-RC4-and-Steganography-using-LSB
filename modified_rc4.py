from typing import List


class ModifiedRC4:
    def __init__(self, in_bytes: List[int], key: str):
        self.in_bytes = in_bytes if in_bytes else []
        self.key = key if key else "KRIPTOGRAFI"

    def encrypt(self) -> List[int]:
        print("encrypting", self.in_bytes[:10], "using", self.key)
        # TODO
        return self.in_bytes

    def decrypt(self) -> List[int]:
        print("decrypting", self.in_bytes[:10], "using", self.key)
        # TODO
        return self.in_bytes
