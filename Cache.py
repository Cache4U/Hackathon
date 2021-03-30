from Database import abstractDatabase, create_fake_dataItem, dataItem
import json
import os


class basicCache(abstractDatabase):
    def delete_data_item(self, item: dataItem):
        self.delete_from_db(item.get_item_id())

    # (cache miss has occurred and we are updating the cache)
    def insert_data_item(self, item: dataItem):
        self.insert_to_or_update_db(item.get_item_id(), item.get_item())

    def __init__(self, location, capacity):
        super().__init__(location)
        self.capacity = capacity

    def delete_from_db(self, key):
        if key not in self.db:
            # Simply do nothing, as the data is not in the db and we just simulate
            pass
        else:
            del self.db[str(key)]
            self.dump_db_to_file()

    def get_from_db(self, key):
        if key in self.db:
            return self.db[str(key)]
        else:
            return None

    # (cache miss has occurred and we are updating the cache) (called from insert)
    def insert_to_or_update_db(self, key, value):
        # LRU algo
        self.db[key] = value
        self.db.move_to_end(key)
        if len(self.db) > self.capacity:
            self.db.popitem(last=False)
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
