import json 

def loadmail():
    try:
        with open("Emails.json", "r") as file:
            emaildict = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        emaildict = {}
    return emaildict

def writeemail(dict):
    with open ("Emails.json", "w") as file:
        json.dump(dict, file)

def registeremail(username, email):
    db = loadmail()
    db[username] = email
    writeemail(db)
    print(f"Email registered {username}, {email}")
    return True

def getemail(username: object) -> object:
    db = loadmail()
    return db[username]