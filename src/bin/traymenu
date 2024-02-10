#!/usr/bin/env python3

"""
A Gtk- or Qt-based menu for the system tray to execute arbitrary commands.
"""

import signal
import sys
import tempfile

import traymenu


DEFAULT_SVG_ICON = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <g style="stroke: #ffffff; stroke-width: 5; stroke-linejoin: round; fill: none">
    <path d="M25,25 L75,25 L25,75 Z"/>
    <path d="M33,47 L47,33"/>
    <path d="M75,75 L45,75 L75,45 Z"/>
  </g>
</svg>
"""


def get_config() -> traymenu.Config:
    """
    Get configuration from command-line arguments.
    """
    try:
        config = traymenu.Config(sys.argv[1:])
        if config.read_menu_items_from_stdin:
            config.set_menu_items_from_file(sys.stdin)
        if not config.menu_items:
            raise ValueError("No menu items given")
        return config

    except ValueError as e:
        usage_str = traymenu.USAGE_STR.replace("traymenu", sys.argv[0], 1)
        print(f"Error: {e}")
        print()
        print(usage_str, end="")
        sys.exit(1)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # enable Ctrl-C in terminal
    config = get_config()
    traymenu.debug_output = config.debug

    with tempfile.TemporaryDirectory() as tmp_dir:

        # Create temporary SVG file if necessary.
        if config.icon_filename is None:
            tmp_icon_file = tmp_dir + "traymenu.svg"
            with open(tmp_icon_file, "w") as fh:
                print(DEFAULT_SVG_ICON, file=fh)
            config.icon_filename = tmp_icon_file

        # Run Gtk or Qt traymenu.
        if config.use_qt:
            import traymenu.qt
            traymenu.qt.run_qt_traymenu(config)
        else:
            import traymenu.gtk
            traymenu.gtk.run_gtk_traymenu(config)
