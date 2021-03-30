from enum import Enum
from collections import List


class Cache:
    def get(self, req):
        return "result"


class DB:
    def get(self, req):
        return "result"


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

    def to_string(self):
        server_dict = {}
        server_dict["curr_queue"] = 0  # change this after implementing queue
        # bank_size = len(self.db.db.keys) # change this after integration with DB
        bank_size = 0  # change this after integration with DB
        server_dict["bank_size"] = bank_size

        cache_sizes = []
        for cache in self.caches:
            cache_sizes.append(0)  # change this after integration with Cache

        server_dict["cache_sizes"] = cache_sizes
        return server_dict
