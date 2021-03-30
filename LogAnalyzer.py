import json
import matplotlib.pyplot as plt
import numpy as np

CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Amber = '#F5B14C'


class LogAnalyzer:
    def __init__(self, logs_path, res_path):
        self.log = Log(path=logs_path)
        self.log.read()
        self.res_path = res_path

    def gen_graphs(self, name):
        self.queue_len_vs_time(name)
        self.avg_user_delay_vs_time(name)

    def queue_len_vs_time(self, sim_name):
        dt = self.log.dt
        log_steps = self.log.log_steps
        queue_lens = [log_steps[t]["server_dict"]["curr_queue"] for t in range(log_steps)]
        plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)), queue_lens)
        plt.savefig()  # save fig to desired path

    def avg_user_delay_vs_time(self, sim_name, window_size=1):
        print("implement this")
        pass
        dt = self.log.dt
        log_steps = self.log.log_steps
        queue_lens = [log_steps[t]["server_dict"]["curr_queue"] for t in range(log_steps)]
        plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)), queue_lens)
        plt.savefig()  # save fig to desired path


class Log:
    def __init__(self, n_users=1, n_madors=1, n_anafs=1, dt=0.01, path=""):
        self.n_users = n_users
        self.n_madors = n_madors
        self.n_anafs = n_anafs
        self.dt = dt
        self.log_steps = []
        self.path = path

    def tick_update(self, server, user_id=-1, user_delay=0):
        """
        This funtion will be called every time tick.
        It will log the information about the current state of the cache, db, queue and users.
        :param server: containing the queue, caches and db
        :param user_id: the user that recieved a result from the server, leave as -1 if no one got an answer
        :param user_delay: the delay of the above result
        :return: None
        """
        log_t = {"server_dict": server.to_string(), "user_id": user_id, "user_delay": user_delay}
        self.log_steps.append(log_t)

    def write(self):
        log_dict = {"n_users": self.n_users, "n_madors": self.n_madors, "n_anafs": self.n_anafs, "dt": self.dt,
                    "log_steps": self.log_steps}
        with open(self.path, 'w') as fp:
            json.dump(log_dict, fp)

    def read(self):
        with open(self.path, 'r') as fp:
            log_dict = json.load(fp)
            self.n_users = log_dict["n_users"]
            self.n_madors = log_dict["n_madors"]
            self.n_anafs = log_dict["n_anafs"]
            self.dt = log_dict["dt"]
            self.log_steps = log_dict["log_steps"]


if __name__ == '__main__':
    dt = 0.01
    log_steps = [1, 2, 3, 4]
    color_list = [CB91_Amber, CB91_Blue, CB91_Green, CB91_Pink, CB91_Purple]
    # plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)), color=CB91_Amber, lw=2.5)
    plt.fill_between(np.linspace(0, dt * len(log_steps), len(log_steps)),
                     np.linspace(0, dt * len(log_steps), len(log_steps)),
                     np.linspace(0, dt * 2 * len(log_steps), len(log_steps)), alpha=0.2, color=CB91_Purple)
    plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)),
             np.linspace(0, dt * 1.5 * len(log_steps), len(log_steps)), color=CB91_Purple, lw=2.5)

    plt.fill_between(np.linspace(0, dt * len(log_steps), len(log_steps)),
                     np.linspace(0, dt * len(log_steps) / 4, len(log_steps)),
                     np.linspace(0, dt * 2 * len(log_steps) / 4, len(log_steps)), alpha=0.2, color=CB91_Blue)
    plt.plot(np.linspace(0, dt * len(log_steps), len(log_steps)),
             np.linspace(0, dt * 1.5 * len(log_steps) / 4, len(log_steps)), color=CB91_Blue, lw=2.5)
    plt.show()
