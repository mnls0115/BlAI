import sys
sys.path.append('/Users/user/Dropbox/2024Projects/BlAI')
# sys.path.append('/Users/mnls0/Dropbox/2024Projects/BlAI')

import configparser
import copy
from Blockchain.Backend.core.block import Block
from Blockchain.Backend.core.blockheader import BlockHeader
from Blockchain.Backend.util.util import hash256, merkle_root, merkle_root_from_hex
from Blockchain.Backend.core.database.database import BlockchainDB, NodeDB, ParameterDB
from Blockchain.Backend.core.Parameters import Parameters
from multiprocessing import Process, Manager
# from Blockchain.Frontend.run import main
import time

Zero_HASH = '0' * 64
VERSION = 1
INITIAL_PARAMETER_NUM = 1250000

class Blockchain:
    def __init__(self, paramPool, Blocksize = None):
        # self.utxos = utxos
        self.paramPool = paramPool
        self.Blocksize = Blocksize if Blocksize is not None else 80
        # self.newBlockAvailable = newBlockAvailable
        # self.secondaryChain = secondaryChain
        # self.current_target = INITIAL_TARGET
        # self.bits = target_to_bits(INITIAL_TARGET)

    def write_on_disk(self, block):
        blockchainDB = BlockchainDB()
        blockchainDB.write(block)

    def fetch_last_block(self):
        blockchainDB = BlockchainDB()
        return blockchainDB.lastBlock()

    def GenesisBlock(self):
        BlockHeight = 0
        prevBlockHash = Zero_HASH
        self.addBlock(BlockHeight = BlockHeight,
                      prevBlockHash = prevBlockHash)
        
    def addBlock(self, BlockHeight, prevBlockHash):
        self.paramPool = ParameterDB().read_and_remove(INITIAL_PARAMETER_NUM)
        self.Blocksize += 8 * len(self.paramPool)
        merkleRoot = merkle_root_from_hex(self.paramPool)[::-1].hex() if self.paramPool != [] else ''
        # merkleRoot = merkle_root(self.paramPool)[::-1].hex()
        timestamp = int(time.time())

        blockHeader = BlockHeader(version = VERSION,
                                  prevBlockHash = prevBlockHash,
                                  merkleRoot = merkleRoot,
                                  timestamp = timestamp)
        blockHeader.mine()
        
        # newBlock = Block(BlockHeight = BlockHeight,
        #                 Blocksize=self.Blocksize,
        #                 BlockHeader=blockHeader,
        #                 Parameters=self.paramPool[:nonce]
        #                 )
                
        self.write_on_disk([Block(BlockHeight = BlockHeight,
                                  Blocksize = self.Blocksize,
                                  BlockHeader = blockHeader.__dict__,
                                  Parameters=self.paramPool
                                  ).__dict__])

    def main(self):
        lastBlock = self.fetch_last_block()
        if lastBlock is None:
            self.GenesisBlock()

        while True:
            lastBlock = self.fetch_last_block()
            BlockHeight = lastBlock["BlockHeight"] + 1
            prevBlockHash = lastBlock["BlockHeader"]["blockHash"]
            self.addBlock(BlockHeight = BlockHeight,
                          prevBlockHash = prevBlockHash)

if __name__ == "__main__":
    blockchain = Blockchain([])
    blockchain.main()