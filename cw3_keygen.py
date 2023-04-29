import hashlib
import random
from rc4 import get_keystream

KEY_MATCH_INT = 89
KEY_MAPPING = ['J', 'N', 'D', 'M', 'G', 'H', 'B', 'K', 'F', 'C', 'P', 'Z', 'R', 'Y', 'W', 'X']
SECRET = "SupportIndieDevelopersWeNeedIt".encode()

def xor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def set_bit(byte_array, pos):
    byte_array[pos >> 3] |= (1 << (pos & 0b111))
    
def interleave_bits(even, odd):
    assert len(even) == len(odd)
    
    b = bytearray(len(even) * 2)

    for i in range(0, len(even) * 8):
        byte_idx = i >> 3
        bit_idx = i & 0b111
        
        if even[byte_idx] >> bit_idx & 1:
            set_bit(b, i * 2)

        if odd[byte_idx] >> bit_idx & 1:
            set_bit(b, i * 2 + 1)
        
    return bytes(b)

def encode_key(key_bytes):
    key = ''.join([KEY_MAPPING[x >> 4] + KEY_MAPPING[x & 0b1111] for x in key_bytes])
    
    for i in range(4, len(key) + 1, 5):
        key = key[:i] + '-' + key[i:]
        
    return key

def generate_key():
    ks = get_keystream(SECRET)
    keystream = bytes(next(ks) for _ in range(16))

    rand_key = (random.randint(0,2**32 // KEY_MATCH_INT) * KEY_MATCH_INT).to_bytes(4, byteorder='little')
    rand_bytes = random.randbytes(4)

    key_bytes = interleave_bits(rand_key, rand_bytes)
    key_hash = hashlib.md5(key_bytes).digest()
    
    return xor(key_bytes + key_hash[0:2], keystream[0:10])

if __name__ == "__main__":
    print("=== CREEPER WORLD 3 KEY GENERATOR ===")

    while True:
        v = input("ENTER:\tGenerate Key\nq+ENTER:\tExit\n")
        
        if v.strip() == "q":
            break
        
        print("\nGenerated Key: " + encode_key(generate_key()) + "\n")
              
