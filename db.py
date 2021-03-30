# TODO: Abstract Database, Database Implementation, and DataItem class

from abc import ABC, abstractmethod
import os


class abstractDatabase(ABC):

    def __init__(self, location):
        self.db_location = os.path.expanduser(location)
        self.load_from_file(self.db_location)

    @abstractmethod
    def load_from_file(self, db_location):
        pass

    @abstractmethod
    def dump_db_to_file(self):
        pass

    @abstractmethod
    def insert_to_db(self, key, value):
        pass

    @abstractmethod
    def get_from_db(self, key):
        pass

    @abstractmethod
    def delete_from_db(self, key):
        pass

