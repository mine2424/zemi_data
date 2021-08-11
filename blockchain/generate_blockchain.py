import hashlib as hasher
import datetime as date

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        # ブロックのindex、timestamp(時間)、data、および前のblockのhashの暗号化ハッシュを生成します。
        # hash_block => '18627f84562249c397955a1bbde617992fea2180afe0e4645ea131df12051a20'
        sha = hasher.sha256()
        sha.update((str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)).encode('utf-8'))
        return sha.hexdigest()


def next_block(last_block):
    this_index = last_block.index + 1
    this_timestamp = date.datetime.now()
    this_data = "Hey! I'm block " + str(this_index)
    this_hash = last_block.hash
    return Block(this_index, this_timestamp, this_data, this_hash)


# ブロックチェーンの最初のブロックを、インデックスが0で、任意の前のハッシュを持つように手動で作成します。
blockchain = [Block(0, date.datetime.now(), "Genesis Block", "0")]
previous_block = blockchain[0]

num_of_blocks_to_add = 20

for i in range(0, num_of_blocks_to_add):
    blocks_to_add = next_block(previous_block)
    blockchain.append(blocks_to_add)
    previous_block = blocks_to_add
    print("Block {} has been added to the blockchain!".format(blocks_to_add.index))
    print("Hash: {}".format(blocks_to_add.hash))
    print("block: {}\n".format(blocks_to_add.data))