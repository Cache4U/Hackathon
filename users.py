import random


class Unit:
    def __init__(self, unit_id, prob = 0):
        self.unit_id = unit_id
        self.prob = prob
        self.past_queries = []
        self.anafs = []

    def add_anaf(self, anaf_id, anaf_prob):
        new_anaf = Anaf(self.unit_id, anaf_id, anaf_prob)
        self.anafs.append(new_anaf)
        return new_anaf

    def generate_query(self,):
        pass


class Anaf:
    def __init__(self, unit, anaf_id, prob = 0):
        self.unit = unit
        self.anaf_id = anaf_id
        self.prob = prob
        self.past_requests = []
        self.madors = []

    def add_mador(self, mador_id, mador_prob):
        new_mador = Mador(self.unit, self.anaf_id, mador_id, mador_prob)
        self.madors.append(new_mador)
        return new_mador

    def generate_request(self):
        pass


class Mador:
    def __init__(self, unit, anaf, mador_id, prob = 0):
        self.unit = unit
        self.anaf= anaf
        self.mador_id = mador_id
        self.prob = prob
        self.past_requests = []
        self.users = []

    def add_user(self, user_id):
        new_user = User(self.unit, self.anaf, self.mador_id, user_id)
        self.users.append(new_user)
        return new_user

    def generate_request(self):
        pass


class User:
    def __init__(self, unit, anaf, mador, user_id, request_rate = 1, prob = 0):
        self.unit = unit
        self.anaf = anaf
        self.mador = mador
        self.user_id = user_id
        self.request_rate = request_rate
        self.prob = prob

    def generate_request(self, unit):
        if random.random() < self.prob:
            return Request(self.unit, self.anaf, self.mador, self.user_id)
        else:
            pass

    def update_request_rate(self, rq):
        self.request_rate = rq


class DataItem:
    def __init__(self):
        pass


class Request:
    def __init__(self, unit_id, anaf_id, mador_id, user_id):
        self.unit_id = unit_id
        self.anaf_id = anaf_id
        self.mador_id = mador_id
        self.user_id = user_id


