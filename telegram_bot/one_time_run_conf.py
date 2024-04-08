# usage 1
"""import json


def write_conf(the_file, data: dict):
    eval_write_file = open(the_file, 'w')

    eval_all = json.dumps(data, indent=4)
    eval_write_file.write(eval_all)
    eval_write_file.close()


def read_conf(new_file: str):

    if new_file:
        the_key = new_file

    config_file = open(new_file, 'r')
    configs = json.loads(config_file.read())
    config_file.close()
    return configs


coins = read_conf('coins.json')
cf = read_conf('coin_follows.json')

for coin in coins['coins']:
    cf[coin] = []

write_conf('coin_follows.json', cf)
"""