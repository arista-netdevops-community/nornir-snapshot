#!/usr/bin/env python3

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir_napalm.plugins.tasks import napalm_cli

import json

nr = InitNornir(config_file='config.yaml')

def get_config(task):
    result = task.run(
        task=napalm_get,
        getters=['config']
    )
    task.run(
        task=write_file,
        content=result.result['config']['running'],
        filename=f'configs/{task.host}.cfg'
    )
    print('Saved ' + f'configs/{task.host}.cfg')

if __name__ == "__main__":
    result = nr.run(task=get_config)
    if result.failed:
        print(result.failed_hosts)
