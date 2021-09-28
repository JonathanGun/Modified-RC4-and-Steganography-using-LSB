import os
import random
from typing import List
from abc import ABC, abstractmethod
from ciphers.vigenere import ExtendedVigenereCipher
from modified_rc4 import ModifiedRC4


class Stego(ABC):
    LEN_META_METABYTE = 3
    IS_MSG_ENCRYPTED_BYTE = 0
    IS_INSERT_RANDOM_BYTE = 1
    LEN_SECRET_FILENAME_BYTE = 2
    SECRET_FILENAME_START_BYTE = 3
    SENTINEL_CNT = 5

    def __init__(
        self,
        secret_bytes: List[int], stego_bytes: List[int],
        key: str, is_msg_encrypted: bool, is_insert_random: bool,
        stego_filepath: str, secret_filepath: str
    ):
        self.secret_bytes = secret_bytes if secret_bytes else []
        self.stego_bytes = stego_bytes if stego_bytes else []
        self.stego_filepath = stego_filepath
        self.stego_filename = os.path.basename(stego_filepath) if stego_filepath else ""
        self.secret_filepath = secret_filepath
        self.secret_filename = os.path.basename(secret_filepath) if secret_filepath else ""
        self.key = key if key else "KRIPTOGRAFI"
        self.is_msg_encrypted = is_msg_encrypted
        self.is_insert_random = is_insert_random
        random.seed(self.key)

    @property
    def secret_header_size(self):
        return self.LEN_META_METABYTE + len(self.secret_filename)

    @abstractmethod
    def _hide(self) -> List[int]:
        pass

    @abstractmethod
    def _extract(self) -> List[int]:
        pass

    def _insert_lsb(self, stego_bytes: List[int], secret_bytes: List[int]) -> List[int]:
        meta_bytes = self._generate_meta_bytes()

        # Validate enough byte on stego to hide msg
        if len(stego_bytes) < (len(meta_bytes) + len(secret_bytes)) * 8:
            raise ValueError('Insufficient bytes, need bigger image / less data')

        # add sentinel chars
        secret_bytes += [ord("#") for _ in range(5)]

        # shuffle secret bytes if random, sequential if not
        insert_sequence = list(range(len(stego_bytes)))
        if self.is_insert_random:
            random.shuffle(insert_sequence)

        # append metadata
        secret_bytes = meta_bytes + secret_bytes
        secret_bytes += stego_bytes[len(secret_bytes):]

        # convert to binary (bits)
        secret_bin = "".join([format(b, "08b") for b in secret_bytes])

        # insert to lsb
        for i, seq in enumerate(insert_sequence):
            stego_bytes[seq] = int(format(stego_bytes[seq], "08b")[:-1] + secret_bin[i], 2)
        return stego_bytes

    def _extract_lsb(self, stego_bytes: List[int]):
        insert_sequence = list(range(len(stego_bytes)))
        if self.is_insert_random:
            random.shuffle(insert_sequence)
        extracted_bins = [format(stego_bytes[seq], "08b")[-1] for seq in insert_sequence]

        # group and convert bits to list of bytes (int)
        extracted_bytes = list(map(lambda x: int(x, 2), ["".join(extracted_bins[i: i + 8]) for i in range(0, len(extracted_bins), 8)]))
        return extracted_bytes

    def _clean_sentinel(self, extracted_bytes: List[int]):
        for i in range(0, len(extracted_bytes) - self.SENTINEL_CNT):
            if extracted_bytes[i] == ord("#"):
                if all(el == ord("#") for el in extracted_bytes[i:i + self.SENTINEL_CNT]):
                    extracted_bytes = extracted_bytes[:i]
                    break
        return extracted_bytes

    def _generate_meta_bytes(self) -> List[int]:
        meta_bytes = []
        meta_bytes.append(int(self.is_msg_encrypted))
        meta_bytes.append(int(self.is_insert_random))
        meta_bytes.append(len(self.secret_filename))
        meta_bytes.extend(ord(s) for s in self.secret_filename)
        return meta_bytes

    def _extract_meta_bytes(self, meta_bytes: List[int]):
        self.is_msg_encrypted = meta_bytes[self.IS_MSG_ENCRYPTED_BYTE]
        self.is_insert_random = meta_bytes[self.IS_INSERT_RANDOM_BYTE]
        secret_filename_bytes = meta_bytes[self.SECRET_FILENAME_START_BYTE: self.SECRET_FILENAME_START_BYTE + meta_bytes[self.LEN_SECRET_FILENAME_BYTE]]
        self.secret_filename = "".join([chr(i) for i in secret_filename_bytes])
        print("extracted meta:", self.is_msg_encrypted, self.is_insert_random, self.secret_filename)

    def hide(self) -> List[int]:
        if self.is_msg_encrypted:
            self.secret_bytes = ModifiedRC4(self.secret_bytes, self.key).encrypt()
        self.out_bytes = self._hide()
        return self.out_bytes

    def extract(self) -> List[int]:
        self.out_bytes = self._extract()
        self._extract_meta_bytes(self.out_bytes)
        self.out_bytes = self._clean_sentinel(self.out_bytes[self.secret_header_size:])
        if self.is_msg_encrypted:
            self.out_bytes = ModifiedRC4(self.out_bytes, self.key).decrypt()
        return self.out_bytes
