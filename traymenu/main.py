#!/usr/bin/env python3
#
# traymenu: A Gtk- or Qt-based menu for the system tray to execute arbitrary
# commands.

import signal
import sys

import traymenu.config
import traymenu.exec


def main() -> None:
    try:
        conf = traymenu.config.get_config(sys.argv[1:])
    except ValueError as e:
        print(e)
        print()
        print("Usage: {sys.argv[0]} qt|gtk [-d|--debug]")
        print("                 --icon <filename>")
        print("               { --item '<label>: <command>' | --separator |")
        print("               { --submenu <label> | --end }")
        sys.exit(1)

    traymenu.exec.debug = conf.debug

    # Enable Ctrl-C on command line.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    if conf.use_qt:
        from traymenu.qt import run_qt_traymenu
        run_qt_traymenu(conf)
    else:
        from traymenu.gtk import run_gtk_traymenu
        run_gtk_traymenu(conf)


if __name__ == "__main__":
    main()
