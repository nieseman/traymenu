#!/usr/bin/env python3
#
# qt.py: Qt-based system tray menu

import functools
import os
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


class TrayIcon(QtWidgets.QSystemTrayIcon):
    """
    Tray icon, which performs 'open context menu' action on both left click and
    right click.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.activated.connect(self.showMenuOnTrigger)

    def showMenuOnTrigger(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.Trigger:
            self.contextMenu().popup(QtGui.QCursor.pos())


def _populate_qt_menu(menu: QtWidgets.QMenu,
                      menu_items: List[config.MenuItem]) -> None:
    """
    Populate given Qt menu object with configured menu items.
    """
    menus = [menu]

    for item in menu_items:
        if isinstance(item, config.Separator):
            menus[-1].addSeparator()

        elif isinstance(item, config.MenuEntry):
            callback = functools.partial(exec.run_command, item.cmd)
            qt_item = menus[-1].addAction(item.label)
            qt_item.triggered.connect(callback)

        elif isinstance(item, config.SubmenuStart):
            qt_submenu = menus[-1].addMenu(item.label)
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

    # Load icon file.
    is_tmp_icon_file, icon_filename = config.get_icon_file(conf.icon_filename)
    qicon = QtGui.QIcon(icon_filename)

    # Work-around: SVG icon is not shown; use a pixmap instead; see:
    # https://bugreports.qt.io/browse/PYSIDE-1493
    qicon = QtGui.QIcon(qicon.pixmap(32))

    # Setup tray icon.
    tray_icon = TrayIcon()
    tray_icon.setContextMenu(menu)
    tray_icon.setIcon(qicon)
    tray_icon.show()

    # Run!
    if is_tmp_icon_file:
        os.remove(icon_filename)
    app.exec_()
