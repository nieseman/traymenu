#!/usr/bin/env python3

"""
Qt-based system tray menu.
"""

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

import traymenu


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
                      menu_items: List[traymenu.MenuItem]) -> None:
    """
    Populate given Qt menu object with configured menu items.
    """
    submenu_stack = [menu]

    for item in menu_items:
        if isinstance(item, traymenu.Separator):
            submenu_stack[-1].addSeparator()

        elif isinstance(item, traymenu.MenuEntry):
            callback = functools.partial(traymenu.run_command, item.cmd)
            qt_item = submenu_stack[-1].addAction(item.label)
            qt_item.triggered.connect(callback)

        elif isinstance(item, traymenu.SubmenuStart):
            qt_submenu = submenu_stack[-1].addMenu(item.label)
            submenu_stack.append(qt_submenu)

        elif isinstance(item, traymenu.SubmenuEnd):
            if len(submenu_stack) > 1:
                submenu_stack.pop()

        else:
            assert False, f"Wrong menu item type: {type(item)}"


def run_qt_traymenu(conf: traymenu.Config) -> None:
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
    # Work-around: SVG icon is not shown; use a pixmap instead; see:
    # https://bugreports.qt.io/browse/PYSIDE-1493
    qicon = QtGui.QIcon(conf.icon_filename)
    qicon = QtGui.QIcon(qicon.pixmap(48))

    # Setup tray icon.
    tray_icon = TrayIcon()
    tray_icon.setContextMenu(menu)
    tray_icon.setIcon(qicon)
    tray_icon.show()

    # Run!
    app.exec_()
