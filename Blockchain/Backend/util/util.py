import hashlib
from Crypto.Hash import RIPEMD160
from hashlib import sha256
from math import log
import numpy as np

BASE58_ALPHABET = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

def hash256(s):
    """SHA 256 두번 함"""
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()

def hash160(s):
    return RIPEMD160.new(sha256(s).digest()).digest()

# def bytes_needed(n):
#     if n == 0:
#         return 1
#     return int(log(n, 256)) + 1

def int_to_little_endian(n, length):
    """Int to little endian takes an integer and return the little-endian byte sequence of length"""
    return n.to_bytes(length, 'little')

def little_endian_to_int(b):
    """takes byte sequence and returns an integer"""
    return int.from_bytes(b, 'little')

# def encode_base58(s):
#     # deretmine how many 0 bytes (b'\x00') s starts with
#     count = 0
#     for c in s:
#         if c == 0:
#             count += 1
#         else:
#             break
#     num = int.from_bytes(s,'big')
#     prefix = '1' * count
#     result = ''
#     while num > 0:
#         num, mod = divmod(num, 58)
#         result = BASE58_ALPHABET[mod] + result
#     return prefix + result

# def decode_base58(s):
#     num = 0

#     for c in s:
#         num *= 58
#         num += BASE58_ALPHABET.index(c)
    
#     combined = num.to_bytes(25, byteorder= 'big')
#     checksum = combined[-4:]

#     if hash256(combined[:-4])[:4] != checksum:
#         raise ValueError(f'bad Adress {checksum} {hash256(combined[:-4][:4])}')
    
#     return combined[1:-4]

def read_variant(s):
    """ read_variant reads a variable integer from a stream """
    i = s.read(1)[0]
    if i == 0xfd:
        # 0xfd means the next two bytes are the number
        return little_endian_to_int(s.read(2))
    elif i == 0xfe:
        # 0xfe means the next four bytes are the number
        return little_endian_to_int(s.read(4))
    elif i == 0xff:
        # 0xff means the next eight bytes are the number
        return little_endian_to_int(s.read(8))
    else:
        # anything else is just the integer
        return i
    
def endcode_variant(i):
    """ Encodes an integer as an variant """
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i,2)
    elif i < 0x100000000:
        return b'\xfe' + int_to_little_endian(i,4)
    elif i < 0x10000000000000000:
        return b'\xff' + int_to_little_endian(i,8)
    else:
        return ValueError(f'Integer too large {i}')
    
def merkle_parent_level(hashes):
    """ Takes a list of binary hashes and returns a list thats half of the length"""
    if len(hashes) % 2 == 1:
        hashes.append(hashes[-1])
    parent_level = []

    for i in range(0,len(hashes), 2):
        parent = hash256(hashes[i] + hashes[i+1])
        parent_level.append(parent)
    return parent_level

def merkle_root(hashes):
    """ Takes a list of binary hashes and returns the merkle root"""
    current_level = hashes
    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)
    
    return current_level[0]

def merkle_root_from_hex(hexs):
    """ Takes a list of binary hashes and returns the merkle root"""
    current_level = [bytes.fromhex(t) for t in hexs]
    while len(current_level) > 1:
        current_level = merkle_parent_level(current_level)
    
    return current_level[0]

# def target_to_bits(target):
#     """ Turns a target integer back into bits """
#     raw_bytes = target.to_bytes(32, 'big')
#     raw_bytes = raw_bytes.lstrip(b'\x00')
#     if raw_bytes[0] > 0x7f:
#         exponent = len(raw_bytes) + 1
#         coefficient = b'\x00' + raw_bytes[:2]
#     else:
#         exponent = len(raw_bytes)
#         coefficient = raw_bytes[:3]
#     new_bits = coefficient[::-1] + bytes([exponent])
#     return new_bits

# def bits_to_target(bits):
#     exponent = bits[-1]
#     coefficient = little_endian_to_int(bits[:-1])
#     return coefficient * 256**(exponent - 3)

# def string_to_bytes(text, fixed_length):
#     # 문자열을 UTF-8로 인코딩
#     text_bytes = text.encode('utf-8')
    
#     # 필요하다면 바이트 스트림을 잘라내거나 패딩 추가
#     if len(text_bytes) < fixed_length:
#         # 부족한 길이만큼 패딩 추가 (여기서는 null 바이트를 사용)
#         text_bytes += b'\x00' * (fixed_length - len(text_bytes))
#     elif len(text_bytes) > fixed_length:
#         # 길이가 초과하면 자름
#         text_bytes = text_bytes[:fixed_length]
#     return text_bytes

def float32_to_bfloat16_bytes(value):
    float32_val = np.float32(value)
    int32_val = float32_val.view(np.int32)
    int16_val = (int32_val >> 16).astype(np.uint16)
    return int16_val.tobytes()  # 16비트 정수를 바이트로 변환

def bfloat16_bytes_to_float32(bfloat16_bytes):
    int16_val = np.frombuffer(bfloat16_bytes, dtype=np.uint16)[0]  # 바이트에서 uint16로 변환
    int32_val = np.uint32(int16_val) << 16
    float32_val = np.int32(int32_val).view(np.float32)
    return float32_val