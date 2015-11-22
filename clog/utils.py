import hashlib


def create_hash(data):
    h = hashlib.sha256()
    h.update(data.encode())
    return h.hexdigest()
