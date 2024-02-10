#!/usr/bin/env python3

"""
Configuration of traymenu program.
"""

from abc import ABC
from dataclasses import dataclass
import os
import tempfile
from typing import List, Optional, Tuple


USAGE_STR = """\
Usage:  traymenu  qt|gtk [-d|--debug] [ --icon <filename> ]
                  ( --stdin | { --item '<label>: <command>' |
                                --submenu <label> |
                                --separator |
                                --submenu-end } )
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
    debug: bool = False
    use_qt: bool = True
    icon_filename: Optional[str] = None
    read_menu_items_from_stdin: bool = False
    menu_items: Optional[List[MenuItem]] = None

    def __init__(self, args: Optional[List[str]] = None) -> None:
        if args is not None:
            self.eval_args(args)

    def eval_args(self, args: List[str]) -> None:
        """
        Get program configuration from command-line arguments
        """
        if not args:
            raise ValueError("No arguments")
        if args[0].lower() not in ("qt", "gtk"):
            raise ValueError("First argument must be 'qt' or 'gtk'")

        self.use_qt = (args[0] == "qt")
        idx = 1
        self.menu_items = []
        while idx < len(args):
            kind, arg = args[idx], args[idx + 1] if idx + 1 < len(args) else None
            if kind in ("--debug", "-d"):
                self.debug = True
                idx += 1
            elif kind == "--icon":
                if arg is None:
                    raise ValueError("Filename for icon missing")
                self.icon_filename = arg
                idx += 2
            elif kind == "--stdin":
                self.read_menu_items_from_stdin = True
                idx += 1
            elif kind == "--separator":
                self.menu_items.append(Separator())
                idx += 1
            elif kind == "--submenu":
                if arg is None:
                    raise ValueError("Name for submenu missing")
                self.menu_items.append(SubmenuStart(arg))
                idx += 2
            elif kind == "--submenu-end":
                self.menu_items.append(SubmenuEnd())
                idx += 1
            elif kind == "--item":
                if arg is None:
                    raise ValueError("Name for menu entry missing")
                pos = arg.find(':')
                label, cmd = arg[:pos], arg[pos + 1:]
                self.menu_items.append(MenuEntry(label.strip(), cmd.strip()))
                idx += 2
            else:
                raise ValueError(f"Bad command-line item '{kind}'")

    @staticmethod
    def unquote(s: str) -> str:
        if len(s) >= 2 and s[0] in ('"', "'") and s[0] == s[-1]:
            return s[1:-1]
        else:
            return s

    def set_menu_items_from_file(self, fh) -> None:
        self.menu_items = []
        for line in fh.readlines():
            line = line.strip()
            if line and line[0] == "#":
                continue

            pos = line.find(' ')
            if pos < 0:
                kind, arg = line, ""
            else:
                kind, arg = line[:pos], self.unquote(line[pos + 1:].strip())

            if kind == "--separator":
                self.menu_items.append(Separator())
            elif kind == "--submenu":
                self.menu_items.append(SubmenuStart(arg))
            elif kind == "--submenu-end":
                self.menu_items.append(SubmenuEnd())
            elif kind == "--item":
                pos = arg.find(':')
                label, cmd = arg[:pos], arg[pos + 1:]
                self.menu_items.append(MenuEntry(label.strip(), cmd.strip()))
            else:
                raise ValueError(f"Bad menu item '{kind}' from stdin")
