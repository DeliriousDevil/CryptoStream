# File: blockchain.py

import hashlib
import time
import json
import random
from typing import List, Optional

class Block:
    """Represents a single block in the blockchain."""
    def __init__(self, index: int, previous_hash: str, transactions: List[dict], nonce: int = 0):
        self.index = index
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = nonce

    def compute_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    """Custom Blockchain with mobile-mining and multi-token support."""
    difficulty = 4  # Adjust for mobile mining balance

    def __init__(self):
        self.chain: List[Block] = []
        self.unconfirmed_transactions: List[dict] = []
        self.tokens: dict = {}  # Multi-token ledger
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [])
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: dict):
        self.unconfirmed_transactions.append(transaction)

    def mine_block(self, miner_address: str) -> Optional[Block]:
        if not self.unconfirmed_transactions:
            return None

        new_block = Block(
            index=len(self.chain),
            previous_hash=self.last_block.compute_hash(),
            transactions=self.unconfirmed_transactions
        )
        self.unconfirmed_transactions = []

        mined = self.proof_of_work(new_block)
        if mined:
            reward_transaction = {"to": miner_address, "amount": 50, "type": "reward"}
            new_block.transactions.append(reward_transaction)
            self.chain.append(new_block)
            return new_block
        return None

    def proof_of_work(self, block: Block) -> bool:
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith("0" * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return True

    def verify_blockchain(self) -> bool:
        for i in range(1, len(self.chain)):
            previous = self.chain[i - 1]
            current = self.chain[i]
            if current.previous_hash != previous.compute_hash():
                return False
            if not current.compute_hash().startswith("0" * Blockchain.difficulty):
                return False
        return True

    def create_token(self, token_name: str, supply: int):
        """Create a new token on the blockchain."""
        if token_name in self.tokens:
            raise ValueError("Token already exists.")
        self.tokens[token_name] = {"supply": supply, "holders": {}}

    def mint_token(self, token_name: str, amount: int, to: str):
        if token_name not in self.tokens:
            raise ValueError("Token does not exist.")
        self.tokens[token_name]["supply"] += amount
        self.tokens[token_name]["holders"][to] = self.tokens[token_name]["holders"].get(to, 0) + amount

    def burn_token(self, token_name: str, amount: int, from_address: str):
        if token_name not in self.tokens:
            raise ValueError("Token does not exist.")
        if self.tokens[token_name]["holders"].get(from_address, 0) < amount:
            raise ValueError("Insufficient balance to burn.")
        self.tokens[token_name]["holders"][from_address] -= amount
        self.tokens[token_name]["supply"] -= amount

to # Example Usage
if __name__ == "__main__":
    blockchain = Blockchain()

    # Add a sample transaction
    blockchain.add_transaction({ “from”: “Alice”, “to”: “Bob”, “amount”: 10, “type”: “transfer"})

    # Mining a block
    miner_block = blockchain.mine_block("Miner1")
    print(f"New block mined: {miner_block.index}")

    # Create a new token
    blockchain.create_token("StreamerCoin", 1000000000)
    blockchain.mint_token("StreamerCoin", 500, "Alice”)
    blockchain.burn_token("StreamerCoin", 100, "Alice”)

    # Validate blockchain integrity
    print(f"Blockchain valid: {blockchain.verify_blockchain()}")
