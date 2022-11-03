#!/usr/bin/env python3
#
# gtk.py: GTK-based system tray menu

import os.path
import sys
from typing import List

try:
    import gi
    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk as gtk
    gi.require_version("AppIndicator3", "0.1")
    from gi.repository import AppIndicator3 as appindicator
except Exception as e:
    print(f"Import error: {e}. Missing module?")
    print("For instance, on Ubuntu: apt install "
          "python3-gi libappindicator3-1 libappindicator3-dev")
    sys.exit(1)

import traymenu.config as config
import traymenu.exec as exec


def _populate_gtk_menu(menu: gtk.Menu, menu_items: List[config.MenuItem]) -> None:
    """
    Populate given Gtk menu object with configured menu items.
    """
    menus = [menu]

    for item in menu_items:
        if isinstance(item, config.Separator):
            gtk_item = gtk.SeparatorMenuItem()
            menus[-1].append(gtk_item)

        elif isinstance(item, config.MenuEntry):
            callback = exec.run_command_wrapper(item.cmd)
            gtk_item = gtk.MenuItem(label=item.text)
            menus[-1].append(gtk_item)
            gtk_item.connect('activate', callback)

        elif isinstance(item, config.SubmenuStart):
            gtk_item = gtk.MenuItem(label=item.text)
            menus[-1].append(gtk_item)
            gtk_submenu = gtk.Menu()
            gtk_item.set_submenu(gtk_submenu)
            menus.append(gtk_submenu)

        elif isinstance(item, config.SubmenuEnd):
            if len(menus) > 1:
                menus.pop()

        else:
            assert False, f"Wrong menu item type: {type(item)}"


def run_gtk_traymenu(conf: config.Config) -> None:
    """
    Create and run the Gtk-based system tray menu.
    """

    # Setup menu.
    tray_menu = gtk.Menu()
    _populate_gtk_menu(tray_menu, conf.menu_items)
    gtk_item = gtk.MenuItem(label='Quit')
    gtk_item.connect('activate', gtk.main_quit)
    tray_menu.append(gtk.SeparatorMenuItem())
    tray_menu.append(gtk_item)

    # Setup tray icon.
    indicator = appindicator.Indicator.new(
        conf.prg_name,
        os.path.abspath(conf.icon_path),    # TBD: if icon_path is not None?
        appindicator.IndicatorCategory.SYSTEM_SERVICES)
    indicator.set_menu(tray_menu)
    indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
    indicator.get_menu().show_all()

    gtk.main()
