#!/usr/bin/env python3
#
# qt.py: Qt-based system tray menu

import functools
import os.path
import sys
from typing import List

try:
    from PyQt5 import QtWidgets, QtGui
except Exception as e:
    print(f"Import error: {e}. Missing module?")
    print("For instance, on Ubuntu: apt install python3-pyqt5")
    sys.exit(1)

import traymenu.config as config
import traymenu.exec as exec


def _populate_qt_menu(menu: QtWidgets.QMenu, menu_items: List[config.MenuItem]) -> None:
    """
    Populate given Qt menu object with configured menu items.
    """
    menus = [menu]

    for item in menu_items:
        if isinstance(item, config.Separator):
            menus[-1].addSeparator()

        elif isinstance(item, config.MenuEntry):
            callback = functools.partial(exec.run_command, item.cmd)
            qt_item = menus[-1].addAction(item.text)
            qt_item.triggered.connect(callback)

        elif isinstance(item, config.SubmenuStart):
            qt_submenu = menus[-1].addMenu(item.text)
            menus.append(qt_submenu)

        elif isinstance(item, config.SubmenuEnd):
            if len(menus) > 1:
                menus.pop()

        else:
            assert False, f"Wrong menu item type: {type(item)}"


def run_qt_traymenu(conf: config.Config) -> None:
    """
    Create and run the Qt-based system tray menu.
    """
    app = QtWidgets.QApplication([conf.prg_name])
    app.setQuitOnLastWindowClosed(False)

    # Setup menu.
    menu = QtWidgets.QMenu()
    _populate_qt_menu(menu, conf.menu_items)
    menu.addSeparator()
    quit_item = menu.addAction('Quit')
    quit_item.triggered.connect(app.quit)

    # Setup tray icon.
    tray_icon = QtWidgets.QSystemTrayIcon()
    tray_icon.setContextMenu(menu)
    if conf.icon_path is not None:
        tray_icon.setIcon(QtGui.QIcon(os.path.abspath(conf.icon_path)))
    tray_icon.setIcon(QtGui.QIcon.fromTheme("system-help"))  # TBD: place-holder
    tray_icon.show()

    app.exec_()
