from Runner import SimulationType
from typing import List


class Cache:
    def get(self, req):
        return "result"


class DB:
    def get(self, req):
        return "result"


class Server:
    def __init__(self, structure: dict, cache_type: SimulationType):
        self.structure = structure

        self.cache_type = cache_type
        self.global_cache = None
        if self.cache_type == SimulationType.GLOBAL.value:
            self.global_cache = Cache()
        else:
            self.caches = {cache_name: Cache() for cache_name in self.get_caches_to_create()}
        self.db = DB()

        self.que = []

    def get_caches_to_create(self) -> List[int]:
        curr_entity = self.structure

        # go deeper for each cache_type
        for _ in range(self.cache_type[0]):
            curr_entity, curr_indexes = self.get_children(curr_entity)

        return curr_indexes

    def get_children(self, entity):
        # for first level
        if type(entity) is dict:
            return list(entity.values()), list(entity.keys())
        # for all other levels - list of sub-entities
        elif type(entity) is list:
            flat_list = []
            for sub_entity in entity:
                flat_list += sub_entity.children

            return flat_list, [child.id for child in flat_list]
        else:
            raise TypeError("Unexpected entity")

    def responder(self, request):
        # handles request

        # find appropriate cache
        if self.cache_type == SimulationType.GLOBAL.value:
            curr_cache = self.global_cache
        else:
            curr_cache = self.caches[getattr(request, self.cache_type[1])]

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

        try:
            curr_req = self.que.pop()
            return self.responder(curr_req)
        except IndexError:
            pass


