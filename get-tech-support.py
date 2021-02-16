#!/usr/bin/env python3

__author__ = 'Petr Ankudinov'

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir_napalm.plugins.tasks import napalm_cli

import json
import os
import re
from getpass import getpass
from time import time as time
from datetime import datetime as datetime

nr = InitNornir(config_file='config.yaml')


def time_stamp():
    """
    time_stamp function returns current system time as Y-M-D H-M-S string

    Args:
        no arguments required

    Returns:
        str: current system time as Y-M-D H-M-S string
    """
    time_not_formatted = time()
    time_formatted = datetime.fromtimestamp(
        time_not_formatted).strftime('%Y-%m-%d:%H:%M:%S.%f')
    return time_formatted


def get_sh_tech(task):
    result = task.run(
        task=napalm_cli,
        # remove any non-printable characters, otherwise task may fail
        commands=['show tech-support | no-more | tr -cd "[:print:][:space:]"']
    )
    task.run(
        task=write_file,
        content=result.result['show tech-support | no-more | tr -cd "[:print:][:space:]"'],
        filename=f'tech_support/{task.host}.txt'
    )
    print('Saved ' + f'tech_support/{task.host}.cfg')
    # add timestamp to the folder
    task.run(
        task=write_file,
        content='> ' + time_stamp(),
        filename=f'tech_support/snapshot-timestamp.md'
    )


if __name__ == "__main__":
    # create base directories if they do not exist
    if not os.path.isdir('tech_support'):
        os.mkdir('tech_support')

    # get username and password to avoid saving them
    username = input("Username: ")
    password = getpass()
    for host in nr.inventory.hosts.values():
        host.username = username
        host.password = password

    result = nr.run(task=get_sh_tech)
    if result.failed:
        print(result.failed_hosts)
