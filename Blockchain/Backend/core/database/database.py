import os
import json

class BaseDB:
    def __init__(self):
        self.basepath = 'data'
        self.filepath = '/'.join((self.basepath, self.filename))

    def read(self):
        if not os.path.exists(self.filepath):
            print(f'file {self.filepath} not abailable')
            return False
        
        with open(self.filepath, 'r') as file:
            raw = file.readline()
        
        if len(raw) > 0:
            data = json.loads(raw)
        else:
            data = []
        return data
    
    def update(self, data):
        with open(self.filepath, 'w+') as f:
            f.write(json.dumps(data))
        return True
    
    def write(self, item):
        data = self.read()
        if data:
            data = data + item
        else:
            data = item
        print(item)

        with open(self.filepath, 'w+') as file:
            file.write(json.dumps(data))

class BlockchainDB(BaseDB):
    def __init__(self):
        self.filename = 'blockchain'
        super().__init__()
    
    def lastBlock(self):
        data = self.read()
        if data:
            return data[-1]
    
    def getBlock(self, BlockHeight):
        data = self.read()
        if data:
            return data[BlockHeight]
        
class AccountDB(BaseDB):
    def __init__(self):
        self.filename = 'account'
        super().__init__()

class NodeDB(BaseDB):
    def __init__(self):
        self.filename = 'node'
        super().__init__()

class ParameterDB(BaseDB):
    def __init__(self):
        self.filename = 'parameters'
        super().__init__()
    
    def read_and_remove(self, num):
        data = self.read()

        # 읽은 후 데이터를 업데이트하여 파일에 다시 쓰기
        remaining_data = data[num:]
        with open(self.filepath, 'w') as file:
            file.write(json.dumps(remaining_data))

        return data[:num]
    
    def write(self, item):
        data = self.read()  # 기존 데이터 읽기
        if data:
            data.append(item)
        else:
            data = [item]

        with open(self.filepath, 'w+') as file:
            file.write(json.dumps(data))