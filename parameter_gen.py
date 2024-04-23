"""
이전 random gen 

import sys
sys.path.append('/Users/user/Dropbox/2024Projects/BlAi')

import random
from Blockchain.Backend.core.Parameters import Parameters, ParameterPosition
from Blockchain.Backend.core.database.database import ParameterDB
from Blockchain.Backend.util.util import float32_to_bfloat16_bytes


BASE58_ALPHABET = '123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

paramnums = 10000
position_array = [(100277, 768),
                  (1024, 768),
                  (768,1),
                  (2304, 768),
                  (2304,1),
                  (768, 768),
                  (3072, 768),
                  (3072,1),
                  (768, 3072)]
WB = ['W', 'B']

if __name__ == '__main__':
    print (len(ParameterDB().read()))
    for idxx in range(paramnums):
        layer,inlayer = random.randint(0,127), random.randint(0,255)
        wb = WB[random.randint(0,1)]
        xy = position_array[random.randint(1,8)]
        position = ParameterPosition(layer=layer,
                                     inlayer=inlayer,
                                     wb=wb,
                                     xy=xy)
        value = 2*random.random()-1
      
        parameters = Parameters(parameterList=[(position, value)]).serialize()
        ParameterDB().write(parameters.hex())
""" 
def tensorbfloat16_to_bytes(bfloat16_tensor):
    # PyTorch 텐서를 NumPy 배열로 변환
    np_array = bfloat16_tensor.numpy()
    # NumPy 배열을 uint16으로 캐스팅
    uint16_array = np_array.view(np.uint16)
    # uint16 배열을 바이트로 변환
    return uint16_array.tobytes()

def tensorbytes_to_bfloat16(byte_data):
    # 바이트 데이터를 np.uint16 배열로 변환
    uint16_array = np.frombuffer(byte_data, dtype=np.uint16)
    # PyTorch의 bfloat16 텐서로 변환
    bfloat16_tensor = torch.from_numpy(uint16_array).to(torch.bfloat16)
    return bfloat16_tensor

import torch
import numpy as np

class Parameter:
    def __init__(self, layer, inlayer, wb, xy, value):
        self.layer = layer
        self.inlayer = inlayer
        self.wb = wb
        self.xy = xy
        self.value = value

inlayers = {'at1': 1,
            'at2': 2,
            'at3': 3,
            'at4': 4,
            'ff1': 5,
            'ff2': 6,
            'ff3': 7,
            'nn1': 8,
            'nn2': 9}

loaded_data = torch.load('/content/drive/MyDrive/2024projects/tensor.pt')
parameterList = []

for name, tensor in loaded_data.items():
    layer, inlayer = (0, 0)  # 기본 값 설정
    wb = 'W'
    x_num = tensor.size(0)
    y_num = tensor.size(1) if tensor.dim() > 1 else 1  # 1차원 텐서 처리

    if name == 'embedding':
        layer = 0
        inlayer = 0
        for x in range(x_num//2):
            for y in range(y_num):
                value = tensor[x, y]
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='W',
                                    xy=(x,y),
                                    value=value)
        for x in range(x_num//2,x_num):
            for y in range(y_num):
                value = tensor[x, y]
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='B',
                                    xy=(x,y),
                                    value=value)

    elif name == 'last1' or 'last2':
        layer = 127
        inlayer = 0
        for x in range(x_num):
                value = tensor[x]
                parameter = Parameter(layer=layer,
                                        inlayer=inlayer,
                                        wb='W',
                                        xy=(x,0),
                                        value=value)

    elif name == 'last2':
        layer = 127
        inlayer = 1
        for x in range(x_num//2):
            for y in range(y_num):
                value = tensor[x, y]
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='W',
                                    xy=(x,y),
                                    value=value)
        for x in range(x_num//2,x_num):
            for y in range(y_num):
                value = tensor[x, y]
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='B',
                                    xy=(x,y),
                                    value=value)
        
    else:
        len = len(name)
        if len == 4:
            layer = int(name[0])
            inlayer = int(inlayers[name[1:4]])
        elif len == 5:
            layer = int(name[0:2])
            inlayer = int(inlayers[name[2:5]])
        else:
            raise ValueError (f"??? {name}, {tensor}")
        
        if y == 1:
            for x in range(x_num):
                value = tensor[x]
                parameter = Parameter(layer=layer,
                                        inlayer=inlayer,
                                        wb='W',
                                        xy=(x,0),
                                        value=value)
        else:
            for x in range(x_num):
                for y in range(y_num):
                    value = tensor[x, y]
                    parameter = Parameter(layer=layer,
                                        inlayer=inlayer,
                                        wb='W',
                                        xy=(x,y),
                                        value=value)
    
    parameterList.append(parameter)
    print(f'name: {name}, layer: {layer}, inlayer: {inlayer}, WB:{wb}, (x,y):{(x,y)}')

# 리스트를 파일로 저장
import pickle

# 파라미터 리스트를 바이너리 파일로 저장
with open('/content/drive/MyDrive/2024projects/parameters.pkl', 'wb') as file:
    pickle.dump(parameterList, file)

# 1at1: tensor([[-2.7618e-03, -2.9053e-02, -3.1586e-03,  ...

