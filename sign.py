#!/usr/bin/env python
from base64 import (
    b64encode,
    b64decode,
)

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA

message = "I want this stream signed"
digest = SHA256.new()
digest.update(message)

# Read shared key from file
private_key = False
with open ("private_key.pem", "r") as myfile:
    private_key = RSA.importKey(myfile.read())

# Load private key and sign message
signer = PKCS1_v1_5.new(private_key)
sig = signer.sign(digest)

# Load public key and verify message
verifier = PKCS1_v1_5.new(private_key.publickey())
verified = verifier.verify(digest, sig)
assert verified, 'Signature verification failed'
print 'Successfully verified message'