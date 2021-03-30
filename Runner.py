from Server import *
from users import *
import numpy as np
import csv
from enum import Enum

timer = 0
structure = {}


class SimulationType(Enum):
    GLOBAL = (0, 'global')
    UNIT = (1, 'unit_id')
    ANAF = (2, 'anaf_id')
    MADOR = (3, 'mador_id')


class Runner:
    global timer
    global structure

    def __init__(self, time_to_run, tick_length, simulation_type):
        self.users = self.create_structure()
        self.server = Server(structure, simulation_type)
        self.time_to_run = time_to_run
        self.tick_length = tick_length

    def create_structure(self):
        global structure
        users = []

        with open('users_conf_sample.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    id = int(row[0])
                    unit_id = int(row[1])
                    anaf_id = int(row[2])
                    mador_id = int(row[3])
                    request_rate = int(row[4])
                    if unit_id not in structure.keys():
                        structure[unit_id] = Unit(unit_id)
                    anaf = structure[unit_id].add_anaf(anaf_id)
                    mador = anaf.add_mador(mador_id)
                    user = mador.add_user(id, request_rate)
                    users.append(user)
                    line_count += 1
        return users

    def run(self):
        global timer
        while timer < self.time_to_run:
            self.generate_action()
            timer += 1
            response = self.server.handle_request()
            if response is not None:
                print('yay i got a response, ' + response)
                pass
            self.sys_to_string()

    def generate_action(self):
        probs = []
        sum_rates = 0
        for user in self.users:
            sum_rates += user.request_rate
            probs.append(user.request_rate)

        p_request_exists = sum_rates*self.tick_length
        probs = [(p/sum_rates)*p_request_exists for p in probs]
        probs.append(1-p_request_exists)
        chosen_user = np.random.choice(self.users+[None], 1, p=probs)[0]
        #print(chosen_user)
        if chosen_user is not None: # else there is no request
            request = chosen_user.generate_request(structure[chosen_user.unit])
            self.server.push_request(request)

    def sys_to_string(self):
        pass


def main():
    r = Runner(20, 0.01, SimulationType.GLOBAL.value)
    r.run()


if __name__ == '__main__':
    main()

