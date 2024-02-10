#!/usr/bin/env python3

"""
Execute arbitrary commands.
"""

import datetime
import subprocess
from typing import Callable


debug_output = False


def run_command(cmd: str):
    """
    Run the given command in the background.
    """
    if debug_output:
        print(f"{datetime.datetime.now().isoformat()}  {cmd} &")
    subprocess.run(f"{cmd} &", shell=True)


def run_command_wrapper(cmd: str) -> Callable:
    """
    Return a function which calls the given command.
    """

    def _run(*unused):
        if debug_output:
            print(f"{datetime.datetime.now().isoformat()}  {cmd} &")
        subprocess.run(f"{cmd} &", shell=True)

    return _run
