import hashlib

hash = "fb2fd2465ef8c1df09616656249fbcc2c84b872eb9ea6a4a5006f07a2a60a78f"

print(hashlib.sha256(hash.decode()).hexdigest())