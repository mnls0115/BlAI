import sys
import struct
import numpy as np

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
# SIGHASH_ALL = 1

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

    @classmethod
    def bytes_to_parameter(cls, byte_data):
        if len(byte_data) != 8 or type(byte_data) != bytes:
            raise ValueError(f"cannot to position due to byte input: {byte_data}")
        
        # struct.unpack을 사용하여 바이트 데이터를 해석
        wb_layer, inlayer, x, y, value_bytes = struct.unpack('<BBHH2s', byte_data)
        value = np.frombuffer(value_bytes, dtype=np.float16).astype(np.float32)[0]

        # W 또는 B 결정
        wb = 'W' if wb_layer < 128 else 'B'
        layer = wb_layer if wb == 'W' else wb_layer - 128
        
        return cls(layer, inlayer, wb, (x, y), value)

    # 이전 to_bytes 함수
    # def to_bytes(self):
    #     # W/B(2) and layer(128) = 1byte, inlayer(256) = 1byte, xy = 4bytes
    #     if self.layer > 127:
    #         raise ValueError (f"cannot to bytes d/t Layer({self.layer}) > 127, ")
        
    #     if self.wb == 0:
    #         result = int_to_little_endian(self.layer, 1)
    #     elif self.wb == 1:
    #         result = int_to_little_endian(self.layer+128, 1)
    #     else:
    #         raise ValueError (f", cannot to bytes d/t WB = {self.wb}")
        
    #     result += int_to_little_endian(self.inlayer, 1)
    #     x, y = self.xy
    #     result += int_to_little_endian(x, 2)
    #     result += int_to_little_endian(y, 2)
    #     result += float32_to_bfloat16_bytes(self.value)
    #     return result

    # @classmethod
    # def bytes_to_parameter(cls, byte):
    #     if len(byte) != 8 or type(byte) != bytes:
    #         raise ValueError (f"cannot to position d/t byte input : {byte}")
    #     wb_layer = byte[0]
    #     wb = 'W' if wb_layer < 128 else 'B'
    #     layer = wb_layer if wb == 'W' else wb_layer - 128
    #     inlayer = byte[1]
    #     x = int.from_bytes(byte[2:4],'little')
    #     y = int.from_bytes(byte[4:6],'little')
    #     value = bfloat16_bytes_to_float32(byte[6:8])

    #     return cls(layer, inlayer, wb, (x, y), value)

class ParameterList:
    command = b'ParameterList'
    def __init__(self, parameterList=None):
        self.parameterList = parameterList if parameterList is not None else []

    def add_parameter(self, parameter):
        if type(parameter) == Parameter:
            self.parameterList.append(parameter)
        else:
            raise ValueError(f"can`t add parameter to ParameterList {parameter}")

    def id(self):
        # Human readable Parameter id
        return self.hash().hex()

    def hash(self):
        # Binary hash of serialization
        return hash256(self.serialize())[::-1]
    
    def serialize(self):
        byte = (len(self.parameterList).to_bytes(4, 'little')
                + b''.join(param.to_bytes() for param in self.parameterList))
        return byte
        
    @classmethod
    def parse(cls, byte_stream):
        # Takes a byte stream and parses the parameter at the start
        # return a parameters onbject
        parameterList = []
        num_params = read_variant(byte_stream)

        for _ in range(num_params):
            byte = byte_stream.read(8)
            parameterList.append(Parameter.bytes_to_parameter(byte))
        return cls(parameterList)

# if __name__ == "__main__":
#     from io import BytesIO
#     parameter = Parameter(127,6,'B',(540,130),1.7109375)
#     param_byte = parameter.to_bytes()
#     print(f"param_byte = {param_byte}")

#     parameter = Parameter(127,6,'B',(540,130),-0.357421875)
#     param_byte = parameter.to_bytes()
#     print(f"param_byte = {param_byte}")

#     print(f"다시 param으로 = {Parameter.bytes_to_parameter(param_byte).__dict__}")

    # parameters = ParameterList(parameterList=[(Parameter(127,6,'B',(540,130),1.7109375)),
    #                                          (Parameter(23,1,'W',(324,23),-1.1328125)),
    #                                          (Parameter(56,32,'B',(242,233),-0.357421875))])
    # parameter_re = parameters.serialize()
    # print(f'parameter_re = {parameter_re}')
    
    # rere = ParameterList.parse(BytesIO(parameter_re))
    # print (rere.__dict__)