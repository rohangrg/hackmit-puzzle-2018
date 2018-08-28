import hashlib
import struct
import os
directory = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(directory, 'words.txt'), 'r') as f:
    WORDS = list(map(lambda x: x.strip().lower(), f.read().strip().split('\n')))

NUM_WORDS = 3

def comhash(secret, username):
    m = hashlib.sha256()
    m.update(username.lower().strip().encode('utf-8'))
    m.update(secret.encode('utf-8'))
    d = m.digest()
    x = struct.unpack('<%dI' % NUM_WORDS, d[0:NUM_WORDS*4])
    return ' '.join(map(lambda i: WORDS[i % len(WORDS)], x))

