import json
import hashlib


def create_hash(data, metadata={}):
    h = hashlib.sha256()
    h.update(data.encode())
    h.update(json.dumps(metadata, sort_keys=True).encode())
    return h.hexdigest()
