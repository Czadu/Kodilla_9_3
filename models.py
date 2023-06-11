import json

class Libraries:
    def __init__(self):
        try:
            with open("libraries.json", "r") as f:
                self.libraries = json.load(f)
        except FileNotFoundError:
            self.libraries = []
    
    def all(self):
        return self.libraries

    def get(self, id):
        try:
            return self.libraries[id - 1]
        except IndexError:
            return None
    
    def create(self, data):
        if 'csrf_token' in data:
            data.pop('csrf_token')
        self.libraries.append(data)

    def save_all(self):
        with open('libraries.json', 'w') as f:
            json.dump(self.libraries, f)

    def update(self, id, data):
        if 'csrf_token' in data:
            data.pop('csrf_token')
        self.libraries[id - 1] = data
        self.save_all()
    
    def delete(self, id):
        try:
            del self.libraries[id - 1]
            self.save_all()
            return True
        except IndexError:
            return False


libraries = Libraries()
    
