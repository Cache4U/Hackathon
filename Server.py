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
        # get response from appropiate cache if available
        curr_cache = self.caches[request.get(cache_type)]

        response = curr_cache.get(request)
        if response:
            return response

        # if not, get from db and update cache with response
        response = self.db.get(request)
        curr_cache.update(request, response)

        return response
