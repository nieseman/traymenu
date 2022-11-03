#!/usr/bin/env python3
#
# config.py: configuration of traymenu program

from abc import ABC
from dataclasses import dataclass
from typing import List, Optional


class MenuItem(ABC):
    """Abstract menu item"""


@dataclass
class Separator(MenuItem):
    """A seperator in the current menu"""


@dataclass
class SubmenuStart(MenuItem):
    """Begin a new submenu in the current menu"""
    text: str


@dataclass
class SubmenuEnd(MenuItem):
    """End the last submenu"""


@dataclass
class MenuEntry(MenuItem):
    """A menu entry for executing a command"""
    text: str
    cmd: str


@dataclass
class Config:
    """Program configuration"""
    prg_name = "TrayMenu"
    debug: bool
    use_qt: bool
    icon_path: Optional[str]
    menu_items: List[MenuItem]


def get_config(args: List[str]) -> Config:
    """Get program configuration from command-line arguments"""
    if not args:
        raise ValueError("No arguments")
    if args[0] not in ("qt", "gtk"):
        raise ValueError("First argument must be 'qt' or 'gtk'")
    use_qt = (args[0] == "qt")
    debug = False
    icon_path = None

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
            icon_path = arg
            idx += 2
        elif kind == "--separator":
            menu_items.append(Separator())
            idx += 1
        elif kind == "--submenu":
            if arg is None:
                raise ValueError("Name for submenu missing")
            menu_items.append(SubmenuStart(arg))
            idx += 2
        elif kind == "--end":
            menu_items.append(SubmenuEnd())
            idx += 1
        elif kind == "--item":
            if arg is None:
                raise ValueError("Name for menu entry missing")
            pos = arg.find(':')
            text, cmd = arg[:pos], arg[pos + 1:]
            menu_items.append(MenuEntry(text.strip(), cmd.strip()))
            idx += 2
        else:
            raise ValueError(f"Bad menu item '{args[0]}'")

    if not menu_items:
        raise ValueError("No menu items given")

    return Config(debug, use_qt, icon_path, menu_items)
