import os
from typing import List
from abc import ABC, abstractmethod
from ciphers.vigenere import ExtendedVigenereCipher


class Stego(ABC):
    def __init__(self, secret_bytes: List[int], stego_bytes: List[int], key: str, is_msg_encrypted: bool, is_insert_random: bool, stego_filepath: str):
        self.secret_bytes = secret_bytes if secret_bytes else []
        self.stego_bytes = stego_bytes if stego_bytes else []
        self.stego_filepath = stego_filepath
        self.stego_filename = os.path.basename(stego_filepath) if stego_filepath else ""
        self.key = key if key else "KRIPTOGRAFI"
        self.is_msg_encrypted = is_msg_encrypted
        self.is_insert_random = is_insert_random
        self.secret_header_size = 3 + len(self.stego_filename)

    def insert(self, stego_bytes: List[int], secret_bytes: List[int]):
        # TODO
        if self.is_insert_random:
            print("inserting to random position")
        else:
            print("inserting to sequential position")
        return stego_bytes

    @abstractmethod
    def _hide(self) -> List[int]:
        pass

    @abstractmethod
    def _extract(self) -> List[int]:
        pass

    def hide(self) -> List[int]:
        if self.is_msg_encrypted:
            self.secret_bytes = ExtendedVigenereCipher(self.secret_bytes, self.key).encrypt()
        # TODO tambah byte pertama: self.is_msg_encrypted
        # TODO tambah byte kedua: self.is_insert_random
        # TODO tambah byte ketiga: len(self.stego_filename)
        # TODO tambah byte keempat - ke-n: self.stego_filename
        out_bytes = self._hide()
        return out_bytes

    def extract(self) -> List[int]:
        # TODO ambil 3 byte pertama
        # TODO ambil byte ke 4 - n buat nama filenya
        # TODO replace in_bytes udah dikurangin itu
        out_bytes = self._extract()
        if self.is_msg_encrypted:
            out_bytes = ExtendedVigenereCipher(out_bytes, self.key).decrypt()
        return out_bytes
