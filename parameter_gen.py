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
import torch
import numpy as np
import json
import struct

class Parameter:
    def __init__(self, layer, inlayer, wb, xy, value):
        self.layer = layer
        self.inlayer = inlayer
        self.wb = wb
        self.xy = xy
        self.value = value

    def to_bytes(self):
        if self.layer > 127:
            raise ValueError(f"Layer value {self.layer} cannot exceed 127.")
        if self.wb not in {'W', 'B'}:
            raise ValueError("Invalid value for wb; it must be 'W' or 'B'.")

        # wb 값을 바이트로 변환하기 전에 처리
        wb_byte = self.layer if self.wb == 'W' else self.layer + 128
        x, y = self.xy

        bfloat16_value = np.float32(self.value).astype(np.float16)
        value_bytes = bfloat16_value.tobytes()

        return struct.pack('<BBHH2s', wb_byte, self.inlayer, x, y, value_bytes)

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
        print(f'embd 진입 : {name}')
        layer = 0
        inlayer = 0
        for x in range(x_num//2):
            for y in range(y_num):
                value = float(tensor[x, y])
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='W',
                                    xy=(x,y),
                                    value=value)
                parameterhex = parameter.to_bytes().hex()
                parameterList.append(parameterhex)
                
        for x in range(x_num//2,x_num):
            for y in range(y_num):
                value = float(tensor[x, y])
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='B',
                                    xy=(x-x_num//2,y),
                                    value=value)
                parameterhex = parameter.to_bytes().hex()
                parameterList.append(parameterhex)

    elif name == 'last1':
        print(f'last1 진입 : {name}')
        layer = 127
        inlayer = 0
        for x in range(x_num):
                value = float(tensor[x])
                parameter = Parameter(layer=layer,
                                        inlayer=inlayer,
                                        wb='W',
                                        xy=(x,0),
                                        value=value)
                parameterhex = parameter.to_bytes().hex()
                parameterList.append(parameterhex)

    elif name == 'last2':
        print(f'last2 진입 : {name}')
        layer = 127
        inlayer = 1
        for x in range(x_num//2):
            for y in range(y_num):
                value = float(tensor[x, y])
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='W',
                                    xy=(x,y),
                                    value=value)
                parameterhex = parameter.to_bytes().hex()
                parameterList.append(parameterhex)

        for x in range(x_num//2,x_num):
            for y in range(y_num):
                value = float(tensor[x, y])
                parameter = Parameter(layer=layer,
                                    inlayer=inlayer,
                                    wb='B',
                                    xy=(x-x_num//2,y),
                                    value=value)
                parameterhex = parameter.to_bytes().hex()
                parameterList.append(parameterhex)

    else:
        len = len(name)
        print(f'name : {name}, len : {len}')
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
                value = float(tensor[x])
                parameter = Parameter(layer=layer,
                                        inlayer=inlayer,
                                        wb='W',
                                        xy=(x,0),
                                        value=value)
                parameterhex = parameter.to_bytes().hex()
                parameterList.append(parameterhex)
        else:
            for x in range(x_num):
                for y in range(y_num):
                    value = float(tensor[x, y])
                    parameter = Parameter(layer=layer,
                                        inlayer=inlayer,
                                        wb='W',
                                        xy=(x,y),
                                        value=value)
                    parameterhex = parameter.to_bytes().hex()
                    parameterList.append(parameterhex)
    
    # 파라미터 리스트를 JSON으로 변환

    with open('/content/drive/MyDrive/2024projects/parameters.json', 'w') as file:
        json.dump(parameterList, file)

    print(f'name: {name}, layer: {layer}, inlayer: {inlayer}, WB:{wb}, (x,y):{(x,y)}, len : {len(parameterList)}')
    print(f'parameters : {parameterList[-10:]}')