import re
import random
import string
from ciphers.base import Cipher


class VigenereCipher(Cipher):
    def __init__(self, msg: str, key: str):
        super().__init__(msg, key)
        self.key = re.sub('[^A-Z]+', '', self.key.upper())
        self.preprocess_key()

    def preprocess_key(self):
        n = len(self.msg) - len(self.key)
        for i in range(n):
            self.key += self.key[i % len(self.key)]

    def _encrypt_single(self, m, k):
        return chr((ord(m) + ord(k)) % 26 + ord("A"))

    def _decrypt_single(self, m, k):
        return chr((ord(m) - ord(k)) % 26 + ord("A"))

    def encrypt(self) -> str:
        cipher_text = []
        for i in range(len(self.msg)):
            cipher_text.append(self._encrypt_single(self.msg[i], self.key[i]))
        cipher_text = cipher_text if self.allow_byte else "".join(cipher_text)
        return cipher_text

    def decrypt(self) -> str:
        plain_text = []
        for i in range(len(self.msg)):
            plain_text.append(self._decrypt_single(self.msg[i], self.key[i]))
        plain_text = plain_text if self.allow_byte else "".join(plain_text)
        return plain_text


class FullVigenereCipher(VigenereCipher):
    def __init__(self, msg: str, key: str):
        super().__init__(msg, key)
        self.generate_lookup_key()

    def generate_lookup_key(self):
        random.seed(self.key)
        uppercase = list(string.ascii_uppercase)
        self.lookup_key = []
        for _ in range(26):
            self.lookup_key.append(random.sample(uppercase, 26))

    def _encrypt_single(self, m, k):
        return self.lookup_key[ord(k) - ord("A")][ord(m) - ord("A")]

    def _decrypt_single(self, m, k):
        return chr(self.lookup_key[ord(k) - ord("A")].index(m) + ord("A"))


class AutoVigenereCipher(VigenereCipher):
    def preprocess_key(self):
        n = len(self.msg) - len(self.key)
        for i in range(n):
            self.key += self.msg[i % len(self.key)]

    def decrypt(self) -> str:
        k = len(self.key)
        # Add decrypted char to key each iteration
        for i in range(len(self.msg)):
            x = self._decrypt_single(self.msg[i], self.key[i])
            self.key += x
        return self.key[k:]


class ExtendedVigenereCipher(VigenereCipher):
    allow_byte = True

    def __init__(self, msg: str, key: str):
        self.msg = msg
        # Cast to list of ASCII int
        if type(self.msg) != list:
            self.msg = [ord(x) for x in self.msg]
        self.key = key.upper()
        self.preprocess_key()

    def _encrypt_single(self, m, k):
        return (m + ord(k)) % 256

    def _decrypt_single(self, m, k):
        return (m - ord(k)) % 256
