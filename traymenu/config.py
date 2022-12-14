#!/usr/bin/env python3
#
# config.py: configuration of traymenu program

from abc import ABC
from dataclasses import dataclass
import os
import tempfile
from typing import List, Optional, Tuple


USAGE_STR = """\
Usage:  traymenu  qt|gtk [-d|--debug] [ --icon <filename> ]
                  { --item '<label>: <command>' | --submenu <label> |
                    --separator | --submenu-end }
"""


class MenuItem(ABC):
    """
    Abstract menu item
    """


@dataclass
class Separator(MenuItem):
    """
    A seperator in the current menu
    """


@dataclass
class SubmenuStart(MenuItem):
    """
    Begin a new submenu in the current menu
    """
    label: str


@dataclass
class SubmenuEnd(MenuItem):
    """
    End the last submenu
    """


@dataclass
class MenuEntry(MenuItem):
    """
    A menu entry for executing a command
    """
    label: str
    cmd: str


@dataclass
class Config:
    """
    Program configuration
    """
    prg_name = "TrayMenu"
    debug: bool
    use_qt: bool
    icon_filename: Optional[str]
    menu_items: List[MenuItem]


def get_config(args: List[str]) -> Config:
    """
    Get program configuration from command-line arguments
    """
    if not args:
        raise ValueError("No arguments")
    if args[0].lower() not in ("qt", "gtk"):
        raise ValueError("First argument must be 'qt' or 'gtk'")
    use_qt = (args[0] == "qt")
    debug = False
    icon_filename = None

    idx = 1
    menu_items = []
    while idx < len(args):
        kind, arg = args[idx], args[idx + 1] if idx + 1 < len(args) else None
        if kind in ("--debug", "-d"):
            debug = True
            idx += 1
        elif kind == "--icon":
            if arg is None:
                raise ValueError("Filename for icon missing")
            icon_filename = arg
            idx += 2
        elif kind == "--separator":
            menu_items.append(Separator())
            idx += 1
        elif kind == "--submenu":
            if arg is None:
                raise ValueError("Name for submenu missing")
            menu_items.append(SubmenuStart(arg))
            idx += 2
        elif kind == "--submenu-end":
            menu_items.append(SubmenuEnd())
            idx += 1
        elif kind == "--item":
            if arg is None:
                raise ValueError("Name for menu entry missing")
            pos = arg.find(':')
            label, cmd = arg[:pos], arg[pos + 1:]
            menu_items.append(MenuEntry(label.strip(), cmd.strip()))
            idx += 2
        else:
            raise ValueError(f"Bad menu item '{kind}'")

    if not menu_items:
        raise ValueError("No menu items given")

    return Config(debug, use_qt, icon_filename, menu_items)


#
# Default icon
#

DEFAULT_SVG_ICON = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <polyline points="25,25 75,25 25,75 25,25" stroke="rgb(255,255,255)" stroke-width="5" stroke-linejoin="round" fill="none"/>
  <polyline points="33,47 47,33"             stroke="rgb(255,255,255)" stroke-width="5" stroke-linejoin="round" fill="none"/>
  <polyline points="45,75 75,45 75,75 45,75" stroke="rgb(255,255,255)" stroke-width="5" stroke-linejoin="round" fill="none"/>
</svg>
"""


def get_icon_file(filename: Optional[str]) -> Tuple[bool, str]:
    """
    If given filename is None, Write the default SVG icon to a new file
    (which is intended to be temporary).
    """
    if filename is None:
        fh, tmp_filename = tempfile.mkstemp(suffix='.svg', text=True)
        with os.fdopen(fh, 'w') as fh:
            print(DEFAULT_SVG_ICON, file=fh)
        return True, tmp_filename
    else:
        return False, filename
