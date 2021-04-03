import Server
from users import User, Unit, Anaf, Mador
# from globals import timer, structure
import numpy as np
import csv
from enum import Enum
from LogAnalyzer import Log, LogAnalyzer


# timer = 0
# structure = {}


class SimulationType(Enum):
    GLOBAL = (0, 'global')
    UNIT = (1, 'unit_id')
    ANAF = (2, 'anaf_id')
    MADOR = (3, 'mador_id')


class Runner:
    # global timer
    # global structure
    def __init__(self, time_to_run, tick_length, simulation_type, sim_name, sim_num, cache_size):
        self.timer = 0
        self.structure = {}
        self.users = self.create_structure()
        self.server = Server.Server(self.structure, simulation_type, cache_size)
        self.time_to_run = time_to_run
        self.tick_length = tick_length
        units = Server.get_children(self.structure)[0]
        anafs = Server.get_children(units)[0]
        madors = Server.get_children(anafs)[0]
        self.logger = Log(len(self.users), len(madors), len(anafs), len(units), "log_dir", sim_name, sim_num)
        self.user_req_probs = self.gen_probs()

    def gen_probs(self):
        probs = []
        sum_rates = 0
        for user in self.users:
            sum_rates += user.request_rate
            probs.append(user.request_rate)

        p_request_exists = sum_rates * self.tick_length
        probs = [(p / sum_rates) * p_request_exists for p in probs]
        probs.append(1 - p_request_exists)
        return probs

    def create_structure(self):
        # global structure
        users = []

        with open('users_conf_real1.csv') as csv_file:
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
                    if unit_id not in self.structure.keys():
                        self.structure[unit_id] = Unit(unit_id)
                    anaf = self.structure[unit_id].add_anaf(anaf_id)
                    mador = anaf.add_mador(mador_id)
                    user = mador.add_user(id, request_rate)
                    users.append(user)
                    line_count += 1
        return users

    def run(self):
        # global timer
        while self.timer < self.time_to_run:
            print(self.timer)
            self.generate_action()
            self.timer += 1
            response = self.server.handle_request(self.timer)
            if response is not None:
                res, handle_time = response
                print('yay i got a response ' + res)
                self.logger.tick_update(self.server, handle_time)
            else:
                self.logger.tick_update(self.server)
            self.sys_to_string()
        self.logger.write()

    def generate_action(self):
        chosen_user = np.random.choice(self.users + [None], 1, p=self.user_req_probs)[0]
        # print(chosen_user)
        if chosen_user is not None:  # else there is no request
            request = chosen_user.generate_request(self.structure[chosen_user.unit])
            self.server.push_request(request, self.timer)

    def sys_to_string(self):
        pass


def main():
    # """
    for i in range(1):
        print("Starting simulation number: {}".format(i + 1))
        r = Runner(15000, 0.001, SimulationType.GLOBAL.value, "real_Global_1800", i, 480)
        r.run()
        r = Runner(15000, 0.001, SimulationType.ANAF.value, "real_Anaf_1800", i, 80)
        r.run()
        # r = Runner(10000, 0.001, SimulationType.MADOR.value, "real_Mador_1800", i, 125)
        r = Runner(15000, 0.001, SimulationType.MADOR.value, "real_Mador_1800", i, 24)
        r.run()
    # """
    LA = LogAnalyzer("log_dir", "real_Global_1800", "results")
    LA.gen_graphs("0")
    LA = LogAnalyzer("log_dir", "real_Mador_1800", "results")
    LA.gen_graphs("0")
    LA = LogAnalyzer("log_dir", "real_Anaf_1800", "results")
    LA.gen_graphs("0")


if __name__ == '__main__':
    main()
