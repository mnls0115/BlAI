import numpy as np

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

# 예제 사용
value = 4.4929038267582655e-10
bfloat16_bytes = float32_to_bfloat16_bytes(value)
restored_float32_val = bfloat16_bytes_to_float32(bfloat16_bytes)

print(f"Original float32: {value}")
print(f"Converted bfloat16 bytes: {bfloat16_bytes}")
print(f"Restored float32: {restored_float32_val}")
