from enum import Enum
import json
import os
from abc import ABC, abstractmethod
from hashlib import sha256
from random import randint

from faker import Faker
from collections import List


class Cache:
    def get(self, req):
        return "result"


class DB:
    def get(self, req):
        return "result"


class dataItem:
    def __init__(self, item):
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
        self.db = {}
        self.db_location = os.path.expanduser(location)
        self.load_from_file(self.db_location)

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
            self.insert_to_or_update_db(random_data_item.get_item_id(), random_data_item.get_item())
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



class CacheType(Enum):
    GLOBAL = 0
    UNIT = 1
    ANAF = 2
    MADOR = 3


class Server:
    def __init__(self, cache_type: CacheType):
        self.cache_type = cache_type
        self.global_cache = None
        if self.cache_type == CacheType.GLOBAL:
            self.global_cache = Cache()
        else:
            self.caches = {cache_name: Cache() for cache_name in self.get_caches_to_create()}
        self.db = DB()

    def get_caches_to_create(self) -> List[str]:
        global structures

        curr_person = structures

        # TODO: handle GLOBAL cache_type

        # go deeper for each cache_type
        for _ in range(int(self.cache_type)):
            # TODO: ask from other team to have children method.
            curr_person = curr_person.children

        return curr_person.to_list()

    def responder(self, request: Request) -> Response:
        # handles request

        # find appropriate cache
        if self.cache_type == CacheType.GLOBAL:
            curr_cache = self.global_cache
        else:
            curr_cache = self.caches[request.get(cache_type)]

        # get response from cache if available
        response = curr_cache.get(request)
        if response:
            return response

        # if not, get from db and update cache with response
        response = self.db.get(request)
        curr_cache.update(request, response)

        return response
