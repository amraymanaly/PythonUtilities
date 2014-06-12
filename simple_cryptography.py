#!/usr/bin/python3
import base64, bz2

def encode(string):
    return base64.b64encode(bz2.compress(bytes(str(string).encode()))).decode()

def decode(string):
    return bz2.decompress(base64.b64decode(bytes(str(string).encode()))).decode()
