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