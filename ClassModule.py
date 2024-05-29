import json

def loadclass(userID):
    try:
        with open("classes.json", "r") as file:
            classdata = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
            classdata = {}
    return classdata

def saveclass(dict):
    with open("classes.json", "w") as file:
        json.dump(dict, file)

def registerclass(userID, classdata):
    db = loadclass()
    db[str(userID)] = classdata
    saveclass(db)
    return True

def getclass(userID):
    db = loadclass()
    return db[userID]
