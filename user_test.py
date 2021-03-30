from users import *


def main():
    Users = []
    prob_new_req = 0.5  # probability of generating a new request
    prob_unit = 0.1  # probability of returning a past request from the unit requests (p = prob_unit*(1-prob_new_req))
    prob_anaf = 0.2  # probability of returning a past request from the anaf requests (p = prob_anaf*(1-prob_unit)*(1-prob_new_req))
    # probability of returning a past request from the mador requests (p = (1-prob_anaf)*(1-prob_unit)*(1-prob_new_req))
    my_unit = Unit(8200, prob_unit)
    anaf_80 = my_unit.add_anaf(80, prob_anaf)
    mador_850 = anaf_80.add_mador(850)
    mador_830 = anaf_80.add_mador(830)
    for i in range(0, 10):
        user_id = random.randint(10000, 90000)
        Users.append(mador_850.add_user(user_id, prob_new_req))
    mador_850.add_user(user_id + 1)

    request = Users[0].generate_request(my_unit)
    print("python main function")


if __name__ == '__main__':
    main()
