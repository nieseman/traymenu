#!/usr/bin/env python3
#
# traymenu: A Gtk- or Qt-based menu for the system tray to execute arbitrary
# commands.

import signal
import sys

from traymenu.config import get_config, USAGE_STR
import traymenu.exec


def main() -> None:

    # Get command-line arguments.
    try:
        conf = get_config(sys.argv[1:])
    except ValueError as e:
        print(e)
        print()
        print(USAGE_STR.replace("traymenu", sys.argv[0], 1), end="")
        sys.exit(1)

    traymenu.exec.debug_output = conf.debug

    # Enable Ctrl-C on command line.
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    # Run traymenu.
    if conf.use_qt:
        from traymenu.qt import run_qt_traymenu
        run_qt_traymenu(conf)
    else:
        from traymenu.gtk import run_gtk_traymenu
        run_gtk_traymenu(conf)


if __name__ == "__main__":
    main()
