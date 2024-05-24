import hashlib
import json

def loadusr():
    try:
        with open('Users.json', 'r') as file:
            userdict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        userdict = {}
    return userdict

def writeusr(dict):
    with open('Users.json', 'w') as file:
        json.dump(dict, file)

def registeruser(username, password):
    db = loadusr()
    if username in db:
        return 0
    else:
        hashpwd = hashlib.sha256(password.encode()).hexdigest()
        db[username] = hashpwd
        writeusr(db)
        print('Registration success')
        return 1

def authuser(username, password):
    db = loadusr()
    if username in db:
        hashedpwd = hashlib.sha256(password.encode()).hexdigest()
        if db[username] == hashedpwd:
            return True
    return False


