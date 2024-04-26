import torch
import numpy as np
import struct
import os

from google.colab import drive
drive.mount('/content/drive')

loaded_data = torch.load('/content/drive/MyDrive/2024projects/tensor.pt')

def bfloat16_to_bytes(tensor):
    # 텐서의 차원 정보를 가져옴
    dimensions = tensor.size()

    # bfloat16 텐서를 float16으로 변환
    tensor_as_float16 = tensor.to(torch.float16)

    # 차원 정보를 32비트 정수로 변환
    dimensions_bytes = struct.pack('<' + 'I' * len(dimensions), *dimensions)

    # 데이터를 바이트로 변환
    data_bytes = tensor_as_float16.numpy().tobytes()

    # 차원 바이트와 데이터 바이트를 결합
    combined_bytes = dimensions_bytes + data_bytes

    # 결합된 바이트 데이터를 16진수 문자열로 변환
    return combined_bytes.hex()

def hex_to_bfloat16_tensor(layername, hex_data):
    # 16진수 데이터를 바이트 데이터로 변환
    byte_data = bytes.fromhex(hex_data)

    # 차원 정보 추출 (32비트 정수로 저장되었다고 가정)
    num_dimensions = 1 if ('nn' in layername or 'last1' in layername) else 2 # 차원 수가 고정된 경우 (예: 2차원 텐서)
    dimensions_bytes_length = 4 * num_dimensions
    dimensions = struct.unpack('<' + 'I' * num_dimensions, byte_data[:dimensions_bytes_length])

    # 실제 데이터는 차원 정보 다음부터 시작
    data_bytes = byte_data[dimensions_bytes_length:]

    # 데이터를 numpy 배열로 변환
    data_array = np.frombuffer(data_bytes, dtype=np.uint16)

    # numpy 배열을 PyTorch의 bfloat16으로 변환
    tensor = torch.from_numpy(data_array.view(np.float16)).to(dtype=torch.bfloat16)

    # 차원 정보를 사용하여 텐서를 원래 차원으로 재구성
    tensor = tensor.view(dimensions)

    print(f'layer: {layername}, dimensions : {dimensions}')

    return tensor

# 이동하려는 파일이 있는 로컬 디렉토리
source_directory = '/content/drive/MyDrive/2024projects/parameterTXT'
# 파일을 이동할 목적지 디렉토리
destination_directory = '/content/drive/MyDrive/2024projects/parameterPT/'

def save_hex_to_file(hex_data, output_file_name):
    # 지정된 폴더 경로
    folder_path = '/content/drive/MyDrive/2024projects/parameterTXT'

    # 전체 파일 경로 조합
    output_file_path = os.path.join(folder_path, output_file_name)

    # 파일 쓰기
    with open(output_file_path, 'w') as file:
        file.write(hex_data)

# 각 레이어별로 파일 저장
for name, param in loaded_data.items():
    hex_representation = bfloat16_to_bytes(param)

    print (name)
    # output_file = f'layer_{name}_bytes_hex.txt'
    # save_hex_to_file(hex_representation, output_file)
    # print(f'{output_file} 으로 저장, length : {len(hex_representation)}')

    # 텐서를 .pt 파일로 저장
def save_tensor_to_pt(tensor, file_name):
    torch.save(tensor, destination_directory + file_name)

# 파일에서 16진수 데이터 읽기
def read_hex_from_file(input_file):
    with open(input_file, 'r') as file:
        hex_data = file.read()
    return hex_data

# source_directory에서 파일 목록 가져오기
files = os.listdir(source_directory)

for file in files:
    input_file = os.path.join(source_directory, file)
    filename = file.replace('_bytes_hex.txt', '') + '_tensor'
    output_file = f'{filename}.pt'

    # 파일에서 16진수 데이터를 읽음
    hex_data = read_hex_from_file(input_file)

    # NumPy 배열을 PyTorch 텐서로 변환
    tensor = hex_to_bfloat16_tensor(filename, hex_data)

    # PyTorch 텐서를 .pt 파일로 저장
    save_tensor_to_pt(tensor, output_file)

    print (f'{filename} 저장됨. tensor: {tensor}')