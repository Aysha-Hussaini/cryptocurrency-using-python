import hashlib
import json

def crypto_hash(*args):
    """
    Return a sha-256 hash of given arguments.
    """
    
    stringified_args = sorted(map( lambda data:json.dumps(data), args))
    joined_data = ''.join(stringified_args)
    
    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()

def main():
    print(f"crypto_hash(1,[5],'three') : {crypto_hash(1,[5],'three')}")

if __name__ == "__main__":
    main()