from Blockchain.Backend.util.util import (hash256,
                                          little_endian_to_int,
                                          int_to_little_endian)
from Blockchain.Backend.core.database.database import BlockchainDB

class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.blockHash = ""

    @classmethod
    def parse(cls, s):
        version = little_endian_to_int(s.read(4))
        prevBlockHash = s.read(32)[::-1]
        merckleRoot = s.read(32)[::-1]
        timestamp = little_endian_to_int(s.read(4))
        return cls(version, prevBlockHash, merckleRoot, timestamp)
    
    def serialize(self):
        result = int_to_little_endian(self.version, 4)
        result += self.prevBlockHash[::-1]
        result += self.merkleRoot[::-1]
        result += int_to_little_endian(self.timestamp, 4)
        return result
    
    # def to_hex(self):
    #     self.blockHash = self.generateBlockHash()
    #     self.prevBlockHash = self.prevBlockHash.hex()
    #     self.merkleRoot = self.merkleRoot.hex()

    # def to_bytes(self):
    #     self.prevBlockHash = bytes.fromhex(self.prevBlockHash)
    #     self.merkleRoot = bytes.fromhex(self.merkleRoot)
    #     self.blockHash = bytes.fromhex(self.blockHash)
    
    def mine(self):
        # newBlockAvailable = False
        # if newBlockAvailable:
        #     competitionOver = True
        #     return competitionOver

        self.blockHash = little_endian_to_int(
                                    hash256(
                                        int_to_little_endian(self.version,4)
                                        + bytes.fromhex(self.prevBlockHash)[::-1]
                                        + bytes.fromhex(self.merkleRoot)[::-1]
                                        + int_to_little_endian(self.timestamp,4)))
        self.blockHash = int_to_little_endian(self.blockHash, 32).hex()[::-1]
    
    # def validateBlock(self):
    #     lastBlock = BlockchainDB().lastBlock()
    #     if self.prevBlockHash.hex() == lastBlock['BlockHeader']['blockHash']:
    #         if self.check_pow():
    #             return True
            
    # def check_pow(self):
    #     sha = hash256(self.serialize())
    #     proof = little_endian_to_int(sha)
    #     return proof < bits_to_target(self.bits)
    
    def generateBlockHash(self):
        sha = hash256(self.serialize())
        proof = little_endian_to_int(sha)
        return int_to_little_endian(proof, 32).hex()[::-1]
    
    def to_dict(self):
        dt = self.__dict__
        return dt