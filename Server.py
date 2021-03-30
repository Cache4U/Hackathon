from Runner import SimulationType
from typing import List
from consts import Consts
# from globals import timer


class Cache:
    def get(self, req):
        return "result"


class DB:
    def get(self, req):
        return "result"


# Get children of structure on each level
def get_children(entity):
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
        self.last_busy_tick = 0

    def get_caches_to_create(self) -> List[int]:
        curr_entity = self.structure

        # go deeper for each cache_type
        for _ in range(self.cache_type[0]):
            curr_entity, curr_indexes = get_children(curr_entity)

        return curr_indexes

    def responder(self, request, timer):
        # handles request

        # if curr_tick - last_active_tick >= cache_ticks
        if timer - self.last_busy_tick >= Consts.CACHE_TICKS:
            # find appropriate cache
            if self.cache_type == SimulationType.GLOBAL.value:
                curr_cache = self.global_cache
            else:
                curr_cache = self.caches[getattr(request, self.cache_type[1])]

            # get response from cache if available
            response = curr_cache.get(request)
            if response:
                return response

        if timer - self.last_busy_tick >= Consts.DB_TICKS:
            # if not, get from db and update cache with response
            response = self.db.get_from_db(request)
            curr_cache.update(request, response)

            return response

        # Not enough ticks! return none
        return None

    def push_request(self, request, timer):
        self.que.append((request, timer))

    def handle_request(self, timer):
        try:
            req, creation_time = self.que[0]

            result = self.responder(req, timer)

            if result:
                self.que = self.que[1:]

                self.last_busy_tick = timer

                # returns result + time of request handling
                return result, timer - creation_time
        # TODO: WTH ???
        except IndexError:
            pass

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
