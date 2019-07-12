import hashlib
import requests
import json
# import boto3

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

def obtain_hash(p):
    encode_p = f'{p}'.encode()
    return hashlib.sha256(encode_p).hexdigest()


def accumulate_hashes(p, hashp, hashdict):
    if hashdict['heads'].get(hashp[:6]) is None:
        hashdict['heads'][hashp[:6]] = []
    if hashdict['tails'].get(hashp[-6:]) is None:
        hashdict['tails'][hashp[-6:]] = []

    hashdict['heads'][hashp[:6]].append(p)
    hashdict['tails'][hashp[-6:]].append(p)


def proof_of_work(last_hash, hashdict):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    start = timer()

    print("Searching for next proof")

    starting_proof = random.randrange(0, (2**64))
    proof = starting_proof
    print("Starting at", proof)

    while validate_proof(last_hash, proof) is False:
        proof +=1
        proof_hash = obtain_hash(proof)
        accumulate_hashes(proof, proof_hash, hashdict)

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof, hashdict


def validate_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    new_hash = obtain_hash(proof)
    if last_hash[-6:] == new_hash[:6]:
        return True
    else:
        return False


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    hashf = open('hashdict.txt', 'r')
    try:
        hashdict = json.load(hashf)
    except json.decoder.JSONDecodeError:
        hashdict = { 'heads': {}, 'tails': {} }
    hashf.close()

    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        last_proof = data.get('proof')
        print(last_proof)
        last_hash = obtain_hash(last_proof)
        if hashdict['heads'].get(last_hash[-6:]):
            new_proof = hashdict['heads'].get(last_hash[-6:])[0]
            new_hashing = False
        else:
            new_proof, hashdict = proof_of_work(last_hash, hashdict)
            new_hashing = True

        print("Trying", new_proof)

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))

        if new_hashing == True:
            hashf = open('hashdict.txt', 'w')
            json.dump(hashdict, hashf)
            hashf.close()
