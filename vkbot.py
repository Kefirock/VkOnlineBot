import vk_api
import random
import time

token = "6d277507e8a0332ce63f4852def78dae23fd9b6d0e7d8fecaf7353ebf576b12c13d7f9d919e8414e2cba3"
vk = vk_api.VkApi(token=token)
vk._auth_token()

session = {}
empty_session = {
    "chat_session": None,
    "uid": None,
    "id_1": None,
    "id_2": None,
    "name1": None,
    "name2": None
}

class ChatSession:
    UID = None
    id_1 = None
    id_2 = None
    name1 = None
    name2 = None

    def __init__(self, name):
        session["chat_session"] = self

        self.UID = random.randint(1, 2147483647)
        session["UID"] = self.UID      

        message = get_message()
        self.id_1 = message[0]
        session["id_1"] = self.id_1

        self.name1 = name
        session["name1"] = self.name1

        write_message(self.UID, self.id_1)

    def connect_user(self):
        pass

def get_username(id):

    user = vk.method("users.get", {"user_ids": id})
    name = user[0]['first_name']
    
    return name

def get_key():
    key = random.randint(1, 2147483647)
    return key

def write_message(message, id):
    vk.method("messages.send", {"peer_id": id, "message": message, "random_id": get_key()})
    
def get_last_message():
    try:
        messages = vk.method("messages.getConversations", {"offset": 0, "count": 20, "filter": "unanswered"})
        #print(messages)

        if messages["count"] >= 1:
            id = messages["items"][0]["last_message"]["from_id"]
            body = messages["items"][0]["last_message"]["text"]

            return id, body
        
        else:
            return None

    except Exception:
        time.sleep(1)

def get_message():
    while True:
        message = get_last_message()

        if message != None:
            id = message[0]
            body = message[1]
        
            return id, body

while True:
    messages = get_last_message()

    if messages != None:
        id = messages[0]
        body = messages[1].lower()
        name = get_username(id)

        if session == {}:
            if body == "начать" or body == "start":

                write_message('Сессия создана. Чтобы завершить её, достаточно написать "стоп".', id)
                write_message('Напишите что-то, чтобы сгенерировать уникальный ключ.', id)
                session = empty_session
                ChatSession(name)
                
            else:
                write_message('Напишите "начать", чтобы начать.', id)
        
        if session != {}:

            if body == "стоп" or body == "stop":
                write_message("Cессия завершена.", id)
                session = {}

            elif body == str(session["uid"]):
                write_message(f"Пользователь {name} подключился к сессии.", id)


                