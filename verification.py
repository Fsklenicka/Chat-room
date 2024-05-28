import random
import EmailHandler

def verify(email):
    code = random.randint(10000, 99999)
    Msg = f'Ověřovací kód pro ChatRoom registraci je:{code}'
    EmailHandler.SendEmail(email, "Oveřovací kód pro ChatRoom")
    return code