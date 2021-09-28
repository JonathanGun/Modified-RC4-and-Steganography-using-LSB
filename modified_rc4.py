from typing import List


class ModifiedRC4:
    def __init__(self, in_bytes: List[int], key: str):
        self.in_bytes = in_bytes if in_bytes else []
        self.key = key if key else "KRIPTOGRAFI"
        self.initstate = [1,0,1] # Inisialisasi register untuk LFSR

    def encrypt(self) -> List[int]:
        print("encrypting", self.in_bytes[:10], "using", self.key)
        lsfr_key = self.lfsr()
        S = self.ksa(self.key)
        i, j = 0, 0
        ciphertext = []
        for idx in range(len(self.in_bytes)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S = self.swap(S, i, j)
            t = (S[i] + S[j]) % 256
            # Modifikasi dengan XOR keystream RC4 dengan keystream LFSR
            u = S[t] ^ lsfr_key
            c = u ^ self.in_bytes[idx]
            ciphertext.append(c)

        return ciphertext

    def decrypt(self) -> List[int]:
        print("decrypting", self.in_bytes[:10], "using", self.key)
        lsfr_key = self.lfsr()
        S = self.ksa(self.key)
        i, j = 0, 0
        plaintext = []
        for idx in range(len(self.in_bytes)):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S = self.swap(S, i, j)
            t = (S[i] + S[j]) % 256
            # Modifikasi - XOR keystream RC4 dengan keystream LFSR
            u = S[t] ^ lsfr_key
            c = u ^ self.in_bytes[idx]
            plaintext.append(c)

        return plaintext

    def ksa(self, key) -> List[int]:
        # KSA
        S = [i for i in range(256)]
        j = 0
        for i in range(256):
            # Modifikasi pada indeks j pada permutasi
            j = (ord(key[j % len(key)]) * j + ord(key[S[i] % len(key)]) * S[i] + ord(key[i % len(key)])) % 256
            S = self.swap(S, i, j)  # swap(S[i],S[j])
        return S

    def swap(self, list, pos1, pos2) -> List[int]:
        list[pos1], list[pos2] = list[pos2], list[pos1]
        return list

    def lfsr(self) -> int:
        '''
            Fungsi umpan balik: melakukan XOR semua bit dalam register kecuali bit ke 8 (MSB)
            Menghasilkan out_bit dengan panjang 2^len(initstate) - 1
            Mengembalikan representasi integer dari out_bit
        '''
        register = self.initstate
        out_bit = []
        for _ in range(pow(len(self.initstate),2)):
            xor = register[1]
            for bit in register[2:]:
                xor ^= bit
            out_bit.append(register.pop())
            register.insert(0, xor)
        # Ubah array bits menjadi representasi integer
        lsfr_keystream = int("".join(str(x) for x in register), 2)
        return lsfr_keystream