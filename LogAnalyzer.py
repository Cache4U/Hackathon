import json
import matplotlib.pyplot as plt
import numpy as np
import os

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Amber = '#F5B14C'


class LogAnalyzer:
    def __init__(self, log_dir, sim_name, res_dir):
        self.path = os.path.join(log_dir, sim_name)
        log_files = os.listdir(self.path)

        self.logs = [Log(file=os.path.join(self.path, log_file)) for log_file in log_files]
        self.dt = self.logs[0].dt
        self.sim_len = len(self.logs[0].log_steps)
        self.res_dir = os.path.join(res_dir, sim_name)
        if not os.path.exists(self.res_dir):
            os.makedirs(self.res_dir)

    def gen_graphs(self, name):
        all_queue_lens = []
        all_users_delays = []
        for log in self.logs:
            curr_queue_lens = self.get_queue_lens(log)
            all_queue_lens.append(np.asarray(curr_queue_lens))
            curr_user_delays = self.get_user_delays(log)
            all_users_delays.append(np.asarray(curr_user_delays))
        all_queue_lens = np.asarray(all_queue_lens)
        all_users_delays = np.asarray(all_users_delays)
        min_queue_lens = all_queue_lens.min(axis=0)
        min_users_delays = all_users_delays.min(axis=0)
        max_queue_lens = all_queue_lens.max(axis=0)
        max_users_delays = all_users_delays.max(axis=0)
        mean_queue_lens = all_queue_lens.mean(axis=0)
        mean_users_delays = all_users_delays.mean(axis=0)

        ts = np.linspace(0, self.dt * self.sim_len, self.sim_len)
        plt.fill_between(ts, min_queue_lens, max_queue_lens)
        plt.plot(ts, mean_queue_lens)
        plt.savefig(os.path.join(self.res_dir, "queue_lens"))
        plt.close('all')

        plt.fill_between(ts, min_users_delays, max_users_delays)
        plt.plot(ts, mean_users_delays)
        plt.savefig(os.path.join(self.res_dir, "users_delays"))
        plt.close('all')

    def get_queue_lens(self, log):
        log_steps = log.log_steps
        queue_lens = [log_steps[t]["server_dict"]["curr_queue"] for t in range(len(log_steps))]
        return queue_lens

    def get_user_delays(self, log):
        print("implement this")
        log_steps = log.log_steps
        user_delays = [log_steps[t]["user_delay"] for t in range(len(log_steps))]
        return user_delays


class Log:
    def __init__(self, n_users=1, n_madors=1, n_anafs=1, dt=0.01, log_dir="", name="default_test", sim_number=0,
                 file=None):
        """
        This class is a log class for one simulation run
        :param n_users: total number of users in the simulation
        :param n_madors: total number of madors in the simulation
        :param n_anafs: total number of  anafs in the simulation
        :param dt: the length of each time tick
        :param log_dir: log_dir path
        :param name: the name of the simulation run
        :param sim_number: the number of the simulation in the current running group
        """
        if file is not None:
            self.load_from_file(file)
            return

        self.n_users = n_users
        self.n_madors = n_madors
        self.n_anafs = n_anafs
        self.dt = dt
        self.log_steps = []
        self.path = os.path.join(log_dir, name)
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        self.sim_number = sim_number

    # def tick_update(self, server, user_id=-1, user_delay=0):
    def tick_update(self, server, user_delay=0):
        """
        This function will be called every time tick.
        It will log the information about the current state of the cache, db, queue and users.
        :param server: containing the queue, caches and db
       ###### :param user_id: the user that recieved a result from the server, leave as -1 if no one got an answer
        :param user_delay: the delay of the above result
        :return: None
        """
        log_t = {"server_dict": server.to_string(), "user_delay": user_delay}
        self.log_steps.append(log_t)

    def write(self):
        log_dict = {"n_users": self.n_users, "n_madors": self.n_madors, "n_anafs": self.n_anafs, "dt": self.dt,
                    "log_steps": self.log_steps}
        json_name = os.path.join(self.path, str(self.sim_number))
        with open(json_name, 'w') as fp:
            json.dump(log_dict, fp)

    def read(self):
        json_name = os.path.join(self.path, str(self.sim_number))
        with open(json_name, 'r') as fp:
            log_dict = json.load(fp)
            self.n_users = log_dict["n_users"]
            self.n_madors = log_dict["n_madors"]
            self.n_anafs = log_dict["n_anafs"]
            self.dt = log_dict["dt"]
            self.log_steps = log_dict["log_steps"]

    def load_from_file(self, file_path):
        with open(file_path, 'r') as fp:
            log_dict = json.load(fp)
            self.n_users = log_dict["n_users"]
            self.n_madors = log_dict["n_madors"]
            self.n_anafs = log_dict["n_anafs"]
            self.dt = log_dict["dt"]
            self.log_steps = log_dict["log_steps"]


if __name__ == '__main__':
    # dt = 0.01
    # log_steps = [1, 2, 3, 4]
    # color_list = [CB91_Amber, CB91_Blue, CB91_Green, CB91_Pink, CB91_Purple]
    # # plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)), color=CB91_Amber, lw=2.5)
    # plt.fill_between(np.linspace(0, dt * len(log_steps), len(log_steps)),
    #                  np.linspace(0, dt * len(log_steps), len(log_steps)),
    #                  np.linspace(0, dt * 2 * len(log_steps), len(log_steps)), alpha=0.2, color=CB91_Purple)
    # plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)),
    #          np.linspace(0, dt * 1.5 * len(log_steps), len(log_steps)), color=CB91_Purple, lw=2.5)
    #
    # plt.fill_between(np.linspace(0, dt * len(log_steps), len(log_steps)),
    #                  np.linspace(0, dt * len(log_steps) / 4, len(log_steps)),
    #                  np.linspace(0, dt * 2 * len(log_steps) / 4, len(log_steps)), alpha=0.2, color=CB91_Blue)
    # plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)),
    #          np.linspace(0, dt * 1.5 * len(log_steps) / 4, len(log_steps)), color=CB91_Blue, lw=2.5)
    # plt.show()
    a1 = np.random.randint(100, size=(5))
    a2 = np.random.randint(100, size=(5))
    a3 = np.random.randint(100, size=(5))
    a4 = np.random.randint(100, size=(5))
    a = np.asarray([a1, a2, a3, a4])
    a_min = a.min(axis=0)
    a_max = a.max(axis=0)
    a_mean = a.mean(axis=0)

    plt.fill_between([1, 2, 3, 4, 5],
                     a_min,
                     a_max, alpha=0.2, color=CB91_Blue)
    plt.plot([1, 2, 3, 4, 5],
             a_mean, color=CB91_Blue, lw=2.5)
    plt.savefig("./test.jpg")
    plt.close('all')
    plt.fill_between([1, 2, 3, 4, 5],
                     a_min,
                     a_max, alpha=0.2, color=CB91_Purple)
    plt.plot([1, 2, 3, 4, 5],
             a_mean, color=CB91_Purple, lw=2.5)
    plt.savefig("./test1.jpg")
