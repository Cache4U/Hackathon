from users import *

def main():
    Users=[]
    my_unit = Unit(8200)
    anaf_80 = my_unit.add_anaf(80)
    mador_850 = anaf_80.add_mador(850)
    mador_830 = anaf_80.add_mador(830)
    for i in range(0, 10):
        user_id = random.randint(10000,90000)
        Users.append(mador_850.add_user(user_id))
    mador_850.add_user(user_id+1)
    request=Users[0].generate_request(my_unit)
    print("python main function")


if __name__ == '__main__':
    main()