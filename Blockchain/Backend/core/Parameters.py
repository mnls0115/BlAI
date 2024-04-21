import sys
sys.path.append('/Users/user/Dropbox/2024Projects/BlAI')
# sys.path.append('/Users/mnls0/Dropbox/2024Projects/BlAI')

from Blockchain.Backend.util.util import (int_to_little_endian,
                                          little_endian_to_int,
                                          endcode_variant,
                                          read_variant,
                                          hash256,
                                          float32_to_bfloat16_bytes,
                                          bfloat16_bytes_to_float32)

# Zero_HASH = b'\0' * 32
# PRIVATEkey = '75164395420649513373157524276748244584997722405728738204141966805748925557554'
# MINER_ADDRESS = '1QtKCDqbCv9EMVIbMgW8q2lij33Cwl2pb'
# SIGHASH_ALL = 1

class ParameterPosition:
    def __init__(self, layer, inlayer, wb, xy):
        self.layer = layer
        self.inlayer = inlayer
        self.wb = 0 if wb == 'W' else 1 if wb == 'B' else None
        self.xy = xy

    def change_to_bytes(self):
        # W/B(2) and layer(128) = 1byte, inlayer(256) = 1byte, xy = 4bytes

        if self.layer > 127:
            raise ValueError (f"cannot to bytes d/t Layer({self.layer}) > 127, ")
        
        if self.wb == 0:
            result = int_to_little_endian(self.layer, 1)
        elif self.wb == 1:
            result = int_to_little_endian(self.layer+128, 1)
        else:
            raise ValueError (f", cannot to bytes d/t WB = {self.wb}")
        
        result += int_to_little_endian(self.inlayer, 1)
        x, y = self.xy
        result += int_to_little_endian(x, 2)
        result += int_to_little_endian(y, 2)

        return result

    @classmethod
    def bytes_to_position(cls, byte):
        if len(byte) != 6 or type(byte) != bytes:
            raise ValueError (f"cannot to position d/t byte input : {byte}")
        wb_layer = byte[0]
        if wb_layer < 128:
            wb = 'W'
            layer = wb_layer
        else:
            wb = 'B'
            layer = wb_layer - 128
        inlayer = byte[1]
        xy = (int.from_bytes(byte[2:4],'little'), int.from_bytes(byte[4:6],'little'))
        return cls(layer, inlayer, wb, xy)

class Parameters:
    command = b'Parameters'
    def __init__(self, parameterList=None):
        self.parameterList = parameterList if parameterList is not None else []

    def add_parameter(self, position, value):
        self.parameterList.append((position,value))

    def id(self):
        # Human readable Parameter id
        return self.hash().hex()

    def hash(self):
        # Binary hash of serialization
        return hash256(self.serialize())[::-1]
    
    def serialize(self):
        result = endcode_variant(len(self.parameterList))

        for paramTuple in self.parameterList:
            if type(paramTuple[0]) != ParameterPosition:
                raise ValueError (f'parameter posision is not right type {paramTuple}')
            result += paramTuple[0].change_to_bytes()
            result += float32_to_bfloat16_bytes(paramTuple[1])

        return result
        
    @classmethod
    def parse(cls, s):
        # Takes a byte stream and parses the parameter at the start
        # return a parameters onbject

        param_num = read_variant(s)
        parameterList = []

        for _ in range(param_num):
            byte = s.read(8)
            parameterList.append((ParameterPosition.bytes_to_position(byte[:6]),
                                  bfloat16_bytes_to_float32(byte[6:8])))
        return cls(parameterList)

# if __name__ == "__main__":
# from io import BytesIO
# #     parameter = ParameterPosition(127,6,'B',(540,130))
# #     param_byte = parameter.change_to_bytes()
# #     print(f"param_byte = {param_byte}")
# #     print(f"다시 param으로 = {ParameterPosition.bytes_to_position(b'\xff\x06\x1c\x02\x82\x00').__dict__}")

#     parameter = Parameters(parameterList=[(ParameterPosition(127,6,'B',(540,130)),0.1234512),
#                                           (ParameterPosition(23,1,'W',(324,23)),0.4632432),
#                                           (ParameterPosition(56,32,'B',(242,233)),0.214653),
#                                           ])
#     parameter_re = parameter.serialize()
#     print(f'parameter_re = {parameter_re}')
    
#     rere = Parameters.parse(BytesIO(parameter_re))
#     print (rere.__dict__)