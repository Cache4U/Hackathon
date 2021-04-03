# TODO: Abstract Database, Database Implementation, and DataItem class

import json
import os
from abc import ABC, abstractmethod
from hashlib import sha256
from collections import OrderedDict
from random import randint

from faker import Faker


class dataItem:
    def __init__(self, item, key=None):
        if key is not None:
            self.id = key
            self.item = item
        else:
            if is_jsonable(item):
                self.item = item
            else:
                self.item = create_fake_dataItem()
            self.id = hash_item(self.item)

    def get_item_id(self):
        return self.id

    def get_item_from_path(self, item_path):
        self.item = json.load(item_path)

    def get_item(self):
        return self.item


def create_fake_dataItem():
    # Generate fake data
    fake = Faker('en_US')
    fake_json = {'name': fake.name(), 'address': fake.address()}
    random_data_item = dataItem(json.dumps(fake_json))
    # Insert fake data item into db, and return the item itself (JSON)
    return random_data_item


def is_jsonable(x):
    try:
        json.dumps(x)
        return True
    except:
        return False


def hash_item(dictionary_item):
    """Kind of a hack, but it works."""
    serialized = json.dumps(dictionary_item, sort_keys=True)
    h = sha256()
    h.update(serialized.encode('utf-8'))
    return h.hexdigest()


class abstractDatabase(ABC):

    def __init__(self, location):
        self.db = OrderedDict()
        self.db_location = os.path.expanduser(location)

    @abstractmethod
    def load_from_file(self, db_location):
        pass

    @abstractmethod
    def dump_db_to_file(self):
        pass

    @abstractmethod
    def insert_to_or_update_db(self, key, value):
        pass

    @abstractmethod
    def get_from_db(self, key):
        pass

    @abstractmethod
    def insert_data_item(self, item: dataItem):
        pass

    @abstractmethod
    def delete_data_item(self, item: dataItem):
        pass

    @abstractmethod
    def delete_from_db(self, key):
        pass


class basicDatabase(abstractDatabase):

    def delete_data_item(self, item: dataItem):
        self.delete_from_db(item.get_item_id())

    def insert_data_item(self, item: dataItem):
        self.insert_to_or_update_db(item.get_item_id(), item.get_item())

    def __init__(self, location):
        super().__init__(location)
        self.load_from_file(self.db_location)

    def delete_from_db(self, key):
        if key not in self.db:
            # Simply do nothing, as the data is not in the db and we just simulate
            pass
        else:
            del self.db[str(key)]
            self.dump_db_to_file()

    def get_from_db(self, key):
        if key not in self.db:
            random_data_item = create_fake_dataItem()
            self.insert_to_or_update_db(key, random_data_item.get_item())
            return random_data_item.get_item()
        else:
            return self.db[str(key)]

    def insert_to_or_update_db(self, key, value):
        self.db[str(key)] = value
        self.dump_db_to_file()

    def dump_db_to_file(self):
        if not os.path.exists(os.path.dirname(self.db_location)):
            os.makedirs(os.path.dirname(self.db_location))
        json.dump(self.db, open(self.db_location, "w+"))

    def load_from_file(self, db_location):
        if os.path.exists(self.db_location):
            self.db = json.load(open(self.db_location, "r"))
        else:
            pass
