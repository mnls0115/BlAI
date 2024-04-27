import numpy as np
import torch
import base64
import io

# 이동하려는 파일이 있는 로컬 디렉토리
PT_directory = '/content/drive/MyDrive/2024projects/parameterPT'
# 파일을 이동할 목적지 디렉토리
JSON_directory = '/content/drive/MyDrive/2024projects/parameterJSON/parameter.json'

# import struct

from google.colab import drive
drive.mount('/content/drive')

loaded_data = torch.load('/content/drive/MyDrive/2024projects/tensor.pt')

# def serialize_tensor(tensor):
#     buffer = io.BytesIO()
#     torch.save(tensor, buffer)
#     buffer.seek(0)
#     return buffer

# def deserialize_tensor(buffer, device='cpu'):
#     buffer.seek(0)  # 버퍼를 읽기 시작하기 전에 데이터 포인터를 시작 위치로 설정
#     tensor = torch.load(buffer, map_location=device)
#     return tensor

def tensor_to_base64(tensor):
    # 텐서를 바이트 스트림으로 직렬화
    buffer = io.BytesIO()
    torch.save(tensor, buffer)
    buffer.seek(0)

    # 바이트 스트림을 base64로 인코딩
    base64_encoded = base64.b64encode(buffer.getvalue())

    # base64 인코딩된 데이터를 UTF-8 문자열로 변환
    return base64_encoded.decode('utf-8')

def base64_to_tensor(base64_string, device='cpu'):
    # base64 문자열을 바이트로 디코드
    decoded_bytes = base64.b64decode(base64_string)

    # BytesIO 스트림 객체 생성
    buffer = io.BytesIO(decoded_bytes)
    buffer.seek(0)  # 버퍼를 읽기 시작하기 전에 데이터 포인터를 시작 위치로 설정

    # deserialize_tensor 함수 사용하여 텐서 로드
    tensor = torch.load(buffer, map_location=device)

    return tensor

import json
import time

def save_tensors_to_json(tensor_dict, file_path):
    start_time = time.time()
    base64_tensors = {}
    for key, tensor in tensor_dict.items():
        base64_string = tensor_to_base64(tensor)
        base64_tensors[key] = base64_string
        print(f'{key} 저장됨. {base64_string[:30]}')
        print(f'시간은 {time.time()-start_time :.2f} 걸렸습니다.')
        start_time = time.time()

    with open(file_path, 'w') as f:
        json.dump(base64_tensors, f)

save_tensors_to_json(loaded_data, JSON_directory)

import json
import time

def load_tensors_from_json(file_path, device='cpu'):
    start_time = time.time()
    with open(file_path, 'r') as f:
        base64_tensors = json.load(f)
    print(f'loading 시 {time.time() - start_time} 걸림.')

    tensor_dict = {}
    for key, base64_string in base64_tensors.items():
        decode_start_time = time.time()
        tensor = base64_to_tensor(base64_string, device)
        tensor_dict[key] = tensor
        print(f'{key} 로드됨. {time.time() - decode_start_time : .2f} 시간 걸림 ')

    return tensor_dict

# 예시 파일 경로
loaded_tensors = load_tensors_from_json(JSON_directory)
print(loaded_data == loaded_tensors)

torch.save(loaded_tensors, PT_directory)