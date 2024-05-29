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
    with open('Users.json', 'a') as file:
        json.dump(dict, file)

def registeruser(username, password):
    db = loadusr()
    if not checkuser(username):
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

def checkuser(username):
    db = loadusr()
    if username in db:
        return False
    else:
        return True

def userlist():
    db=loadusr()
    return list(db.keys())

def changepassword(username, password):
    db = loadusr()
    print(username)
    if username in db:
        # Debugging: Print statements to verify the function execution
        print(f"Changing password for {username}")
        hashepwd = hashlib.sha256(password.encode()).hexdigest()
        print(f"New hashed password: {hashepwd}")
        del db[username]
        db[username] = hashepwd
        writeusr(db)
        return True
    else:
        print(f"Username {username} not found")
        return False


