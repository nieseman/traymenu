# traymenu
<image align="right" width="100" src="doc/traymenu.png">
A Gtk/Qt-based menu for the system tray to execute arbitrary commands.

It takes some inspiration from the "alltray" tool
(https://alltray.sourceforge.net/, https://linux.die.net/man/1/alltray).

*What does it look like?*

Screenshot in Kubuntu, using the Qt menu:
```
$ CMD_TERM="xterm -geometry 80x30 -hold -bg black -fg green -e"
$ traymenu qt --debug \
    --submenu "Test/sysinfo" \
        --item "disk free: $CMD_TERM df" \
        --separator \
        --item "mount: $CMD_TERM mount" \
        --submenu-end \
    --item "uptime: $CMD_TERM uptime"
```

![Screenshot](doc/traymenu_screenshot_qt.png)

*Help!?*

```
$ traymenu
No arguments

Usage:  traymenu  qt|gtk [-d|--debug] [ --icon <filename> ]
                  { --item '<label>: <command>' | --submenu <label> |
                    --separator | --submenu-end }
```
