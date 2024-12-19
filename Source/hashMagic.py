from PIL import Image
import imagehash

HASH_SIZE = 12 # Size of computed hash

def calculate_hash(file):
    im = Image.open(file)
    h = imagehash.average_hash(im, HASH_SIZE)
    return h

def is_similar(hash1, hash2, threshold=90):
    diff_limit = int(((1 - threshold/100)*(HASH_SIZE**2)))

    hamming_dist = abs(hash1 - hash2)
    if hamming_dist <= diff_limit:
        return True
    return False
