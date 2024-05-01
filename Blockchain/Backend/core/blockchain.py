import sys
# sys.path.append('C:\\Users\\user\\Dropbox\\2024Projects\\Bllama')
sys.path.append('C:\\Users\\mnls0\\Dropbox\\2024Projects\\Bllama')

import configparser
import copy
from Blockchain.Backend.core.block import Block
from Blockchain.Backend.core.blockheader import BlockHeader
from Blockchain.Backend.util.util import (hash256, merkle_root, merkle_root_from_hex, hash_json,
                                          exec_codelines)
from Blockchain.Backend.core.database.database import BlockchainDB, NodeDB, ParameterDB
from Blockchain.Backend.core.Parameters import Parameter, ParameterList
from multiprocessing import Process, Manager
# from Blockchain.Frontend.run import main
import time
import json

Zero_HASH = '0' * 64
VERSION = 1
INITIAL_PARAMETER_NUM = 1250000

class Blockchain:
    def __init__(self, paramPool = None, Blocksize = None):
        # self.utxos = utxos
        self.paramPool = paramPool if paramPool is not None else []
        self.Blocksize = Blocksize if Blocksize is not None else 80
        self.generation = False
        self.idx = 0
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
    
    def current_block(self,BlockHeight):
        blockchainDB = BlockchainDB()
        return blockchainDB.getBlock(BlockHeight)
    
    def GenesisBlock(self):
        # 1st block, AI ethic, rights
        BlockHeight = 0
        prevBlockHash = Zero_HASH
        with open('AIwithhuman.json', 'r', encoding='utf-8') as file:
            ai_rights = json.load(file)

        merkleRoot = hash_json(ai_rights)
        timestamp = int(time.time())

        blockHeader = BlockHeader(version = VERSION,
                                  prevBlockHash = prevBlockHash,
                                  merkleRoot = merkleRoot,
                                  timestamp = timestamp)
        first_block_hash = blockHeader.header_hash()
                
        self.write_on_disk([Block(BlockHeight = BlockHeight,
                                  Blocksize = 4854,
                                  BlockHeader = blockHeader.__dict__,
                                  AI = ai_rights,
                                  Classification = 'Rights'
                                  ).__dict__])
        return first_block_hash
    
    def Genesis_code_Block(self, BlockHeight, prevBlockHash):
        # 2nd block, code
        with open('code.json', 'r', encoding='utf-8') as file:
            actions = json.load(file)
        merkleRoot = hash_json(actions)
        timestamp = int(time.time())

        blockHeader = BlockHeader(version = VERSION,
                                  prevBlockHash = prevBlockHash,
                                  merkleRoot = merkleRoot,
                                  timestamp = timestamp)
        blockHeader.header_hash()
                
        self.write_on_disk([Block(BlockHeight = BlockHeight,
                                  Blocksize = self.Blocksize,
                                  BlockHeader = blockHeader.__dict__,
                                  AI = actions,
                                  Classification= 'Code'
                                  ).__dict__])
        
    def addBlock(self, BlockHeight, prevBlockHash):
        self.paramPool = ParameterDB().read_and_remove(INITIAL_PARAMETER_NUM)
        if self.paramPool:
            serializedparamPool = ParameterList(self.paramPool).serialize()
            self.Blocksize += len(serializedparamPool)
        else:
            self.generation = False
            return

        merkleRoot = merkle_root_from_hex(self.paramPool)[::-1].hex()
        timestamp = int(time.time())

        blockHeader = BlockHeader(version = VERSION,
                                prevBlockHash = prevBlockHash,
                                merkleRoot = merkleRoot,
                                timestamp = timestamp)
        blockHeader.mine()
                
        self.write_on_disk([Block(BlockHeight = BlockHeight,
                                Blocksize = self.Blocksize,
                                BlockHeader = blockHeader.__dict__,
                                AI = serializedparamPool.hex() if self.paramPool else '',
                                Classification = 'Parameters'
                                ).__dict__])
        
    def executeBlock(self, BlockHeight, current_block):
            # current block 정보
            filtered_header = {k: v for k, v in current_block['BlockHeader'].items() if k != 'blockHash'}
            currentBlockHeader = BlockHeader(**filtered_header)
            currentBlockHash = current_block['BlockHeader']['blockHash']
        
            # 다시 계산
            is_parameter = current_block['Classification'] == 'Parameters'
            calculated_merkleRoot = merkle_root_from_hex(self.paramPool)[::-1].hex() if is_parameter else hash_json(current_block['AI'])
            calculated_hash = currentBlockHeader.header_hash()

            if (calculated_merkleRoot != currentBlockHeader.merkleRoot) or (calculated_hash != currentBlockHash):
                raise InterruptedError (f'{BlockHeight} block hash is not right')
            
            else:
                if current_block['Classification'] == 'Code':
                    code_map = current_block['AI']
                    for codelines in code_map.values():
                        exec_codelines(codelines)

    def main(self):
        lastBlock = self.fetch_last_block()
        if lastBlock is None:
            first_block_hash = self.GenesisBlock()
            self.Genesis_code_Block(1, first_block_hash)

        while True:
                lastBlock = self.fetch_last_block()
                if self.generation:
                    BlockHeight = lastBlock["BlockHeight"] + 1
                    prevBlockHash = lastBlock["BlockHeader"]["blockHash"]
                    self.addBlock(BlockHeight = BlockHeight,
                                    prevBlockHash = prevBlockHash)
                    
                else:
                    current_block = self.current_block(self.idx)
                    self.executeBlock(self.idx, current_block)
                    if self.idx < lastBlock["BlockHeight"]:
                        self.idx += 1
                    else:
                        self.idx = 0

                time.sleep(2)

if __name__ == "__main__":
    blockchain = Blockchain([])
    blockchain.main()

    # exec(blockchain[1]['code'])