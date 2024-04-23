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
inlayers = {'at1': 1,
            'at2': 2,
            'at3': 3,
            'at4': 4,
            'ff1' : 5,
            'ff2' : 6,
            'ff3' : 7,
            'nn1' : 8,
            'nn2' : 9}

loaded_data = torch.load('/content/drive/MyDrive/2024projects/tensor.pt')
for name, tensor in loaded_data.items():
    if name == 'embedding':
        pass
    else:
        layer = int(name[0])
        inlayer = inlayers[name[1:4]]
        wb = 'W'
        x_num, y_num = tensor.size()
        for x in range(x_num):
            for y in range(y_num):
                value = tensor[x, y] 


# 1at1: tensor([[-2.7618e-03, -2.9053e-02, -3.1586e-03,  ...

