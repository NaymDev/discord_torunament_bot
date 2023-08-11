import datetime
import json

class User:
    def __init__(self, name, igname=""):
        self.name = name
        self.igname = igname
        self._timeout_received = None
        self._timeout_time = None
    
    def auth_timeout(self, time=1):
        self._timeout_received = datetime.datetime.now()
        self._timeout_time = time
    
    def is_timeout(self):
        if self._timeout_received is None or self._timeout_time is None:
            return False
        
        remaining_time = (self._timeout_received + datetime.timedelta(0, self._timeout_time*60) - datetime.datetime.now()).total_seconds() / 60.0
        
        return remaining_time >= 0
    
    def remaining_time_string(self):
        if self._timeout_received is None or self._timeout_time is None:
            return "Timeout not set."
        
        if not self.is_timeout():
            return "Timeout has finished."
        
        remaining_time = (self._timeout_received + datetime.timedelta(0, self._timeout_time*60) - datetime.datetime.now())
        
        if remaining_time.days > 0:
            return f"{remaining_time.days}d {remaining_time.seconds // 3600}h"
        elif remaining_time.seconds >= 3600:
            return f"{remaining_time.seconds // 3600}h {(remaining_time.seconds % 3600) // 60}min"
        elif remaining_time.seconds >= 60:
            return f"{remaining_time.seconds // 60}min {remaining_time.seconds % 60}s"
        else:
            return f"{remaining_time.seconds}s"
        

def save_data(path):
    file = path.replace(".", "/") + ".json"
    data = {"teams":{}}
    for id, user in USER.items():
        user_data = {
            "name": user.name,
            "igname": user.igname
        }
        data[id] = user_data
    
    for name, user in TEAMS.items():
        data["teams"][name] = user

    with open(file, "w") as f:
        json.dump(data, f)

def read_data(path):
    global USER
    file = path.replace(".", "/") + ".json"
    with open(file, "r") as f:
        data = json.load(f)
    
    for key, value in data.items():
        if key.isdigit(): #Key is a user id
            USER[int(key)] = User(name=data[key]["name"], igname=data[key]["igname"])
    for key, value in data["teams"].items():
        TEAMS[key] = value


USER = {
}

TEAMS = {
}