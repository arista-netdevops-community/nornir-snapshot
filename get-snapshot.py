#!/usr/bin/env python3

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
    # add timestamp to the folder
    task.run(
        task=write_file,
        content='> ' + time_stamp(),
        filename=f'configs/snapshot-timestamp.md'
    )


def run_a_command_list(task, a_command_list):
    result = task.run(
        task=napalm_cli,
        commands=a_command_list
    )
    for a_command in a_command_list:
        # find all words in a command to remove all non-printable characters
        word_list = re.findall(r"[\w]+", a_command)
        # build sub directory name
        sub_dir_name = ''
        while word_list:
            sub_dir_name += word_list.pop(0)
            if word_list:  # if not the last word, add separator
                sub_dir_name += '-'
        dir_name = f'show_commands/{sub_dir_name}'
        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
        # write a command output to a file
        task.run(
            task=write_file,
            content=result.result[a_command],
            filename=f'{dir_name}/{task.host}.txt'
        )
        print('Saved ' + f'{dir_name}/{task.host}.txt')
        # add timestamp to the folder
        task.run(
            task=write_file,
            content='> ' + time_stamp(),
            filename=f'{dir_name}/snapshot-timestamp.md'
        )


if __name__ == "__main__":
    # create base directories if they do not exist
    if not os.path.isdir('configs'):
        os.mkdir('configs')
    if not os.path.isdir('show_commands'):
        os.mkdir('show_commands')

    # get username and password to avoid saving them
    username = input("Username: ")
    password = getpass()
    for host in nr.inventory.hosts.values():
        host.username = username
        host.password = password

    result = nr.run(task=get_config)
    if result.failed:
        print(result.failed_hosts)

    snapshot_command_list = list()
    with open('snapshot_commands.txt', 'r') as snapshot_commands_file:
        snapshot_command_list = [a_line.strip()
                                 for a_line in snapshot_commands_file]

    result = nr.run(task=run_a_command_list,
                    a_command_list=snapshot_command_list)
    if result.failed:
        print(result.failed_hosts)
        print_result(result)
