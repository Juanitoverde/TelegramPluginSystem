import json
import os

class Database:
    def __init__(self, file_path):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            self._data = {}
            self.save()
        else:
            with open(self.file_path, 'r') as f:
                self._data = json.load(f)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def update(self, key, value):
        if key in self._data:
            self._data[key].update(value)
            self.save()

    def delete(self, key):
        if key in self._data:
            del self._data[key]
            self.save()

    def save(self):
        with open(self.file_path, 'w') as f:
            json.dump(self._data, f, indent=4)
