from uuid import uuid4
from collections import OrderedDict

import binascii
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

MINING_DIFFICULTY = 1

# import requests

class Transaction:
    def __init__(self, sender_address, sender_private_key, recipient_address, value):
        self.sender_address = sender_address
        self.sender_private_key = sender_private_key
        self.recipient_address = recipient_address
        self.value = value

    def __getattr__(self, attr):
        return self.data[attr]

    def to_dict(self):
        return OrderedDict(
            {'sender_address': self.sender_address,
            'recipient_address': self.recipient_address,
            'value' : self.value})

    def sign_transaction(self):
        """Sign the transaction with sender's private key"""
        private_key = RSA.importKey(binascii.unhexlify(self.sender_private_key))
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf-8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')

class Blockchain:
    def __init__(self):
        self.transactions = []
        self.chain = []
        self.nodes = set()
        # Random number to use as node id
        self.node_id = str(uuid4()).replace('-', '')
        # Genesis block
        self.create_block_and_add_to_chain(0, '00')

    def register_node(self, node_url):
        """
        Add new node to the list of nodes
        """
        pass

    def verify_transaction_signature(self, sender_address, signature, transaction):
        """
        Verifies that provided signature corresponds to transaction signed by
        the public key (sender address)
        """
        pass

    def submit_transaction(self, sender_address, recipient_address, value, signature):
        """
        Add verified transaction to the transaction array
        """
        pass

    def create_block_and_add_to_chain(self, nonce, previous_hash):
        """
        Add a block of transactions to the blockchain
        """
        pass

    @staticmethod
    def hash(block):
        """
        Create SHA-256 hash of a block
        """
        return

    # @staticmethod
    def proof_of_work(self):
        """
        Proof of work algorithm
        """
        pass

    def valid_proof(self, transactions, last_hash, nonce, difficulty=MINING_DIFFICULTY):
        """
        Check whether hash value satisfies mining conditions. This function is used within the proof_of_work function.
        """
        pass

    def valid_chain(self, chain):
        """
        Check whether blockchain is valid
        """
        pass

    def resolve_conflicts(self):
        """
        Resolve conflicts between blockchain's nodes
        by replacing our chain with the longest one in the network.
        """
        pass
