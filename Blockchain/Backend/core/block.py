from Blockchain.Backend.core.blockheader import BlockHeader
from Blockchain.Backend.core.Parameters import Parameters
from Blockchain.Backend.util.util import (int_to_little_endian,
                                          little_endian_to_int,
                                          endcode_variant,
                                          read_variant)

class Block:
    """ Block is a storage container that stores transactions """

    command = b'block'

    # txs > parameters, txcount > 제거, nonce > 제거
    def __init__(self, BlockHeight, Blocksize, BlockHeader, Parameters, code = None):
        self.BlockHeight = BlockHeight
        self.Blocksize = Blocksize
        self.BlockHeader = BlockHeader
        self.Parameters = Parameters
        self.code = code if code is not None else None

    """
    @classmethod
    def parse(cls, s):
        BlockHeight = little_endian_to_int(s.read(4))
        BlockSize = little_endian_to_int(s.read(4))
        blockHeader = BlockHeader.parse(s) 
        ParamCount = read_variant(s)

        Parameters = []
        for _ in range(ParamCount):
            Parameters.append(Parameters.parse(s))
        
        return cls(BlockHeight,BlockSize,blockHeader,ParamCount,Parameters)

    def serialize(self):
        result = int_to_little_endian(self.BlockHeight, 4)
        result += int_to_little_endian(self.Blocksize, 4)
        result += self.BlockHeader.serialize()
        result += endcode_variant(len(self.Parameters))

        for param in self.Parameters:
            result += param.serialize()
        
        return result
        
    @classmethod
    def to_object(cls, lastblock):
        block = BlockHeader(lastblock['BlockHeader']['version'],
                    bytes.fromhex(lastblock['BlockHeader']['prevBlockHash']),
                    bytes.fromhex(lastblock['BlockHeader']['merkleRoot']),
                    lastblock['BlockHeader']['timestamp'],
                    bytes.fromhex(lastblock['BlockHeader']['bits']))
        
        Parameters = []
        for param in lastblock['Parameters']:
            Parameters.append(Tx.to_obj(tx))
        
        block.blockHash = bytes.fromhex(lastblock['BlockHeader']['blockHash'])
        return cls(lastblock['BlockHeight'],
                   lastblock['Blocksize'],
                   block,
                   len(Transactions),
                   Transactions)
    """
    
    def to_dict(self):
        dt = self.__dict__
        self.BlockHeader = self.BlockHeader.to_dict()
        return dt
