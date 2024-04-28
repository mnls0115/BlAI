import torch
import base64
import io
import json
import os
import gzip

# 이동하려는 파일이 있는 로컬 디렉토리
PT_directory = '/content/drive/MyDrive/2024projects/parameterPT'
# 파일을 이동할 목적지 디렉토리
JSON_directory = '/content/drive/MyDrive/2024projects/parameterJSON/parameter.json'

# import struct

from google.colab import drive
drive.mount('/content/drive')

loaded_data = torch.load('/content/drive/MyDrive/2024projects/tensor.pt')


# 기본 함수
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

# base64 및 gzip 저장
def save_data_gzipped(data, filename):
    # 데이터를 JSON으로 변환 후 gzip을 사용하여 압축하고 파일로 저장
    with gzip.GzipFile(filename, 'w') as f:
        f.write(json.dumps(data, indent=4).encode('utf-8'))

def split_json_file(output_folder):
    # Process the first layer (embedding layer)
    embd_value = loaded_data['embedding']
    embedding_value = tensor_to_base64(embd_value)
    filename = os.path.join(output_folder, f'layer_000_embedding.json.gz')
    save_data_gzipped({'layer_embedding': embedding_value}, filename)

    # Process remaining layers
    index = 0
    current_batch = {}
    file_number = 0

    for name, tensor in loaded_data.items():
        if name == 'embedding':
            continue

        base64_tensor = tensor_to_base64(tensor)
        current_batch[f'layer_{name}'] = base64_tensor
        index += 1

        # Save every 72 layers after the first layer
        if index  % 72 == 0 and index > 1:
            pre1 = '00' if file_number < 2 else '0'
            pre2 = '00' if file_number < 1 else '0'
            filename = os.path.join(output_folder, f'layer_{pre1}{file_number*8+1}_{pre2}{file_number*8+8}.json.gz')
            save_data_gzipped(current_batch, filename)
            current_batch = {}
            file_number += 1

    # Process any remaining layers not saved
    if current_batch:
        filename = os.path.join(output_folder, 'layer_127_last.json.gz')
        save_data_gzipped(current_batch, filename)

output_folder = '/content/drive/MyDrive/2024projects/parameterJSON/'
split_json_file(output_folder)

def read_gzip_json(filename):
    # gzip 파일을 열고 JSON 데이터를 읽습니다
    with gzip.open(filename, 'rt', encoding='utf-8') as f:
        data = json.load(f)
    return data

def reconstruct_tensor_map(input_folder):
    tensor_map = {}
    # input_folder 내의 모든 파일을 순회합니다
    for filename in os.listdir(input_folder):

        if filename.endswith('.gz'):
            full_path = os.path.join(input_folder, filename)
            data = read_gzip_json(full_path)

            # 각 레이어의 텐서를 복원합니다
            for layer_name, base64_string in data.items():
                layer_name = layer_name[6:]
                tensor = base64_to_tensor(base64_string)
                tensor_map[layer_name] = tensor

    return tensor_map

input_folder = '/content/drive/MyDrive/2024projects/parameterJSON/jsongz'
tensor_map = reconstruct_tensor_map(input_folder)

# Tensor 2개 비교하는 함수
def compare_tensor_maps(tensor_map_1, tensor_map_2, atol=1e-08, rtol=1e-05):
    if set(tensor_map_1.keys()) != set(tensor_map_2.keys()):
        print("Tensor maps have different sets of layers.")
        return False

    for key in tensor_map_1.keys():
        tensor1 = tensor_map_1[key]
        tensor2 = tensor_map_2[key]
        if not torch.allclose(tensor1, tensor2, atol=atol, rtol=rtol):
            print(f"Tensor values for layer {key} do not match.")
            return False

    print("All tensors match.")
    return True


# 파일 1mb 씩 읽어오기
def load_data_gzipped_in_chunks(filename, chunk_size=1024*1024):
    file_number = 0

    # gzip 파일 열기
    with gzip.GzipFile(filename, 'rb') as f:
        while True:
            # 1MB 크기의 데이터 블록 읽기
            chunk = f.read(chunk_size)
            if not chunk:
                break

            ## chunk를 블록에 1mb씩 저장하는 함수 추가하기 ##
            file_number += 1

# 파일명 지정 및 데이터 로딩
filename = 'layer_017_024.json.gz'