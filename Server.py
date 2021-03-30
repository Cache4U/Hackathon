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

        self.que = []

    def get_caches_to_create(self) -> List[str]:
        global structures

        curr_person = structures

        # TODO: handle GLOBAL cache_type

        # go deeper for each cache_type
        for _ in range(self.cache_type.value):
            # TODO: ask from other team to have children method.
            curr_person = curr_person.children

        return curr_person.to_list()

    def responder(self, request):
        # handles request

        # find appropriate cache
        if self.cache_type == CacheType.GLOBAL:
            curr_cache = self.global_cache
        else:
            curr_cache = self.caches[request.get(self.cache_type)]

        # get response from cache if available
        response = curr_cache.get(request)
        if response:
            return response

        # if not, get from db and update cache with response
        response = self.db.get(request)
        curr_cache.update(request, response)

        return response

    def push_request(self, request):
        self.que.append(request)

    def handle_request(self):
        # req = que.top

        # if curr_tick - last_active_tick >= cache_ticks
        # go to cache

        # if curr_tick - last_active_tick >= db_ticks
        # go to db

        # que.pop()

        # last_active_tick = now

        curr_req = self.que.pop()
        return self.responder(curr_req)
