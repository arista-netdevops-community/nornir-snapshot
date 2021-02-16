#!/usr/bin/env python3

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from nornir_napalm.plugins.tasks import napalm_cli

import json
import os
import re

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
            sub_dir_name += word_list.pop()
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


if __name__ == "__main__":
    result = nr.run(task=get_config)
    if result.failed:
        print(result.failed_hosts)

    result = nr.run(task=run_a_command_list, a_command_list=['show version'])
    if result.failed:
        print(result.failed_hosts)
        print_result(result)
