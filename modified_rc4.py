from typing import List


class ModifiedRC4:
    def __init__(self, in_bytes: List[int], key: str):
        self.in_bytes = in_bytes if in_bytes else []
        self.key = key if key else "KRIPTOGRAFI"

    def encrypt(self) -> List[int]:
        print("encrypting", self.in_bytes[:10], "using", self.key)
        # TODO
        S = self.ksa(self.key)
        i, j = 0, 0
        ciphertext = []
        for idx in range(len(self.in_bytes)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S = self.swap(S, i, j)
            t = (S[i] + S[j]) % 256
            u = S[t]
            c = u ^ self.in_bytes[idx]
            ciphertext.append(c)
        # self.in_bytes = ciphertext
        return ciphertext

    def decrypt(self) -> List[int]:
        print("decrypting", self.in_bytes[:10], "using", self.key)
        # TODO
        S = self.ksa(self.key)
        i, j = 0, 0
        plaintext = []
        for idx in range(len(self.in_bytes)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S = self.swap(S, i, j)
            t = (S[i] + S[j]) % 256
            u = S[t]
            c = u ^ self.in_bytes[idx]
            plaintext.append(c)
        # self.in_bytes = plaintext
        return plaintext

    def ksa(self, key) -> List[int]:
        # KSA
        S = [i for i in range(256)]
        j = 0
        for i in range(256):
            j = (j + S[i] + ord(key[i % len(key)])) % 256
            S = self.swap(S, i, j)  # swap(S[i],S[j])
        return S

    def swap(self, list, pos1, pos2) -> List[int]:
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list
