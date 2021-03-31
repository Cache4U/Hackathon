import random
import copy
import json
from hashlib import sha256

class Unit:
    def __init__(self, unit_id, prob=0):
        self.unit_id = unit_id
        self.prob = prob
        self.past_requests = []
        self.anafs = []

    def update_req(self, req, anaf_id, mador_id):
        self.past_requests.append(req)
        for anaf in self.anafs:
            if anaf.anaf_id == anaf_id:
                anaf.update_req(req, mador_id)

    def add_anaf(self, anaf_id, anaf_prob=0):
        for anaf in self.anafs:
            if anaf.anaf_id == anaf_id:
                return anaf
        new_anaf = Anaf(self.unit_id, anaf_id, anaf_prob)
        self.anafs.append(new_anaf)
        return new_anaf

    def generate_requests(self, anaf_id, mador_id):
        if random.random() < self.prob:
            # todo return fresher requests
            return random.choice(self.past_requests)

        else:
            for anaf in self.anafs:
                if anaf.anaf_id == anaf_id:
                    return anaf.generate_request(mador_id)

    @property
    def children(self):
        return self.anafs

    @property
    def id(self):
        return self.unit_id


class Anaf:
    def __init__(self, unit, anaf_id, prob=0.1):
        self.unit = unit
        self.anaf_id = anaf_id
        self.prob = prob
        self.past_requests = []
        self.madors = []

    def update_req(self, req, mador_id):
        self.past_requests.append(req)
        for mador in self.madors:
            if mador.mador_id == mador_id:
                mador.update_req(req)

    def add_mador(self, mador_id, mador_prob=0):
        for mador in self.madors:
            if mador.mador_id == mador_id:
                return mador
        new_mador = Mador(self.unit, self.anaf_id, mador_id, mador_prob)
        self.madors.append(new_mador)
        return new_mador

    def generate_request(self, mador_id):
        if random.random() < self.prob:
            # todo return fresher requests
            return random.choice(self.past_requests)

        else:
            for mador in self.madors:
                if mador.mador_id == mador_id:
                    return mador.generate_request()

    @property
    def children(self):
        return self.madors

    @property
    def id(self):
        return self.anaf_id


class Mador:
    def __init__(self, unit, anaf, mador_id, prob=0.7):
        self.unit = unit
        self.anaf = anaf
        self.mador_id = mador_id
        self.prob = prob
        self.past_requests = []
        self.users = []

    def update_req(self, req):
        self.past_requests.append(req)

    def add_user(self, user_id, request_rate=1):
        for user in self.users:
            if user.user_id == user_id:
                return user
        new_user = User(self.unit, self.anaf, self.mador_id, user_id, request_rate)
        self.users.append(new_user)
        return new_user

    def generate_request(self):
        return random.choice(self.past_requests)

    @property
    def children(self):
        return self.users

    @property
    def id(self):
        return self.mador_id


class User:
    def __init__(self, unit, anaf, mador, user_id, request_rate=1, prob=0.2):
        self.unit = unit
        self.anaf = anaf
        self.mador = mador
        self.user_id = user_id
        self.request_rate = request_rate
        self.prob = prob

    def generate_request(self, unit):
        mador = get_mador(unit, self.anaf, self.mador)
        if random.random() < self.prob or len(mador.past_requests)==0 or mador.past_requests is None:
            req = Request(self.unit, self.anaf, self.mador, self.user_id)
            unit.update_req(req, self.anaf, self.mador)
            return req
        else:
            req = copy.deepcopy(unit.generate_requests(self.anaf, self.mador))
            req.unit_id = self.unit
            req.anaf_id = self.anaf
            req.mador_id = self.mador
            req.user_id = self.user_id
            return req

    def update_request_rate(self, rq):
        self.request_rate = rq

    @property
    def id(self):
        return self.user_id


class DataItem:
    def __init__(self):
        pass


global_counter = 0


def hash_item(dictionary_item):
    """Kind of a hack, but it works."""
    serialized = json.dumps(dictionary_item, sort_keys=True)
    h = sha256()
    h.update(serialized.encode('utf-8'))
    return h.hexdigest()


class Request:
    def __init__(self, unit_id, anaf_id, mador_id, user_id):
        global global_counter
        self.unit_id = unit_id
        self.anaf_id = anaf_id
        self.mador_id = mador_id
        self.user_id = user_id
        self.query = hash_item(global_counter)
        global_counter += 1


def get_mador(unit, anaf_id, mador_id):
    for anaf in unit.anafs:
        if anaf.anaf_id == anaf_id:
            for mador in anaf.madors:
                if mador.mador_id == mador_id:
                    return mador
