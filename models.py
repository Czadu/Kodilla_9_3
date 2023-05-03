import json

class Librarys:
    def __init__(self):
        try:
            with open("librarys.json", "r") as f:
                self.librarys = json.load(f)
        except FileNotFoundError:
            self.librarys = []
    
    def all(self):
        return self.librarys

    def get(self, id):
        return self.librarys[id]
    
    def create(self, data):
        data.pop('csrf_token')
        self.librarys.append(data)

    def save_all(self):
        with open('librarys.json', 'w') as f:
            json.dump(self.librarys, f)

    def update (self, id, data):
        data.pop('csrf_token')
        self.librarys[id] = data
        self.save_all()


librarys = Librarys()
    
