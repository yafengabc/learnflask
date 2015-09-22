import os
import hashlib

def hashfile(path):
    haskey=hashlib.md5()
    for i in open(path,'rb'):
        haskey.update(i)
    return haskey.hexdigest()


