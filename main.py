def create_baller(id_baller, name, value):
    return {
        "id_baller": id_baller,
        "name": name,
        "value": value
    }


def get_id_baller(baller):
    return baller["id_baller"]


def get_name(baller):
    return baller["name"]


def get_value(baller):
    return baller["value"]


def equal_ballers(baller_a, baller_b):
    return get_id_baller(baller_a) == get_id_baller(baller_b)


def to_string_baller(baller):
    return f"{get_id_baller(baller)} {get_name(baller)} {get_value(baller)}"

def test_create_baller():
    print("starting domain tests...")
    id_baller = 23
    name = "Jordan"
    value = 9000.1
    epsilon = 0.0001
    baller = create_baller(id_baller, name, value)
    assert get_id_baller(baller) == id_baller
    assert get_name(baller) == name
    assert abs(get_value(baller) - value) < epsilon
    print("finishing domain tests...")


def validate_baller(baller):
    errors = ""
    if get_id_baller(baller) < 0:
        errors += "invalid id!\n"
    if get_name(baller) == "":
        errors += "invalid name!\n"
    if get_value(baller) <= 0.0:
        errors += "invalid value!\n"
    if len(errors) > 0:
        raise Exception(errors)


def test_validate_baller():
    print("starting validate tests...")
    id_baller = -23
    name = ""
    value = -9000.1
    epsilon = 0.0001
    baller = create_baller(id_baller, name, value)
    try:
        validate_baller(baller)
        assert False
    except Exception as ex:
        assert str(ex) == "invalid id!\ninvalid name!\ninvalid value!\n"
    print("finishing validation tests...")


def add_baller_to_team(team, baller):
    if get_id_baller(baller) in team:
        raise Exception("existing baller!")
    team[get_id_baller(baller)] = baller


def srv_add_baller_to_team(team, id_baller, name, value):
    baller = create_baller(id_baller, name, value)
    validate_baller(baller)
    add_baller_to_team(team, baller)


def get_baller_by_id(team, id_baller):
    if id_baller not in team:
        raise Exception("inexisting baller!")
    return team[id_baller]


def get_all_ballers(team):
    return [team[id_baller] for id_baller in team]


def test_add_baller_to_team():
    print("starting repo tests...")
    team = {}
    id_baller = 23
    name = "Jordan"
    value = 9000.1
    baller = create_baller(id_baller, name, value)

    add_baller_to_team(team, baller)
    assert len(team) == 1
    found_baller = get_baller_by_id(team, id_baller)
    assert equal_ballers(found_baller, baller)
    try:
        add_baller_to_team(team, baller)
        assert False
    except Exception as ex:
        assert str(ex) == "existing baller!"
    id_baller = 24
    name = "Kobe"
    value = 9000.05
    other_baller = create_baller(id_baller, name, value)
    add_baller_to_team(team, other_baller)
    ballaz = get_all_ballers(team)
    ballaz.sort(key=lambda x: get_id_baller(x))
    assert ballaz[0] == baller
    assert ballaz[1] == other_baller
    print("finishing repo tests...")


def run_tests():
    test_create_baller()
    test_validate_baller()
    test_add_baller_to_team()


def ui_add_baller(team, params):
    if len(params) != 3:
        print("invalid no of params!")
        return
    try:
        id_baller = int(params[0])
        name = params[1]
        value = float(params[2])
        srv_add_baller_to_team(team, id_baller, name, value)
    except ValueError:
        raise Exception("invalid numerical value!")


def ui_print_team(team, params):
    if len(params) != 0:
        print("invalid no of params!")
        return
    for baller in get_all_ballers(team):
        print(to_string_baller(baller))

def run():
    team = {}
    commands = {
        "add_balla": ui_add_baller,
        "print_team": ui_print_team
    }
    while True:
        cmd = input(">>>")
        cmd = cmd.strip()
        if cmd == "":
            continue
        if cmd == "exit":
            return
        parts = cmd.split()
        cmd_name = parts[0]
        params = parts[1:]
        if cmd_name in commands:
            try:
                commands[cmd_name](team, params)
            except Exception as ex:
                print(ex)
        else:
            print("invalid command!")


def main():
    run_tests()
    run()


main()
