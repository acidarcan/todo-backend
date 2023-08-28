import os
import json

def print_with_indent(value, indent=0):
    indentation = '\t' * indent
    print(f'{indentation}{value}')

class Entry:
    def __init__(self, title, entries=None, parent=None):
        self.title = title
        if entries is None:
            entries = []
        self.entries = entries
        self.parent = parent

    def add_entry(self, entry):
        self.entries.append(entry)
        entry.parent = self

    def print_entries(self, indent=0):
        print_with_indent(self, indent)
        for entry in self.entries:
            entry.print_entries(indent=indent + 1)

    def json(self):
        res = {
            'title': self.title,
            'entries': [entry.json() for entry in self.entries]
        }
        return res

    def save(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

        filename = os.path.join(path, f'{self.title}.json')
        with open(filename, 'w') as file:
            json.dump(self.json(), file, indent=4)

    def __str__(self):
        return self.title

    @classmethod
    def from_json(cls, value):
        entry = cls(value['title'])
        for sub_entry in value.get('entries', []):
            sub_entry_instance = cls.from_json(sub_entry)
            entry.add_entry(sub_entry_instance)
        return entry

    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as file:
            data = json.load(file)
            return cls.from_json(data)

if __name__ == "__main__":
    root_data = {
        "title": "Root",
        "entries": [
            {
                "title": "Entry 1",
                "entries": [
                    {
                        "title": "Subentry 1"
                    }
                ]
            },
            {
                "title": "Entry 2"
            }
        ]
    }

    root = Entry.from_json(root_data)

    save_path = "/tmp"
    root.save(save_path)

    loaded_root = Entry.load(os.path.join(save_path, "Root.json"))
    loaded_root.print_entries()


class EntryManager:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.entries = []

    def save(self):
        for entry in self.entries:
            entry.save(self.data_path)

    def load(self):
        for filename in os.listdir(self.data_path):
            if filename.endswith(".json"):
                full_path = os.path.join(self.data_path, filename)
                loaded_entry = Entry.load(full_path)
                self.entries.append(loaded_entry)

    def add_entry(self, title: str):
        new_entry = Entry(title)
        self.entries.append(new_entry)


data_path = "путь_к_вашим_данным"
entry_manager = EntryManager(data_path)

entry_manager.add_entry("Новая запись")