#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import gettext
import subprocess
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QUrl
from PyQt5.QtCore import QSize
from xdg.IconTheme import getIconPath
from utils.pyjs import Pyjs

# get translations
gettext.install("kcenter", "/usr/share/locale/kcenter")

if __name__ == "__main__":

    # Create application QT and create WebView
    app = QApplication([])
    web = QWebView()

    # Get current theme
    command = "kreadconfig --group 'Icons' --key 'Theme'"
    theme = subprocess.getoutput(command)

    # Set Title
    title = _("Kaiana Control Panel")
    web.setWindowTitle(title)

    # Set icon
    icon = QIcon()
    icon.addFile(getIconPath('preferences-system', theme=theme, size=16), QSize(16,16))
    icon.addFile(getIconPath('preferences-system', theme=theme, size=32), QSize(32,32))
    icon.addFile(getIconPath('preferences-system', theme=theme, size=64), QSize(64,64))
    icon.addFile(getIconPath('preferences-system', theme=theme, size=256), QSize(256,256))
    web.setWindowIcon(icon)


    # Center Window
    web.move(app.desktop().screen().rect().center() - web.rect().center())

    # Show Debug
    if "--debug" in sys.argv:
        debug = True
    else:
        debug = False

    if debug:

        # Enable extra tools for developers
        from PyQt5.QtWebKit import QWebSettings
        web.page().settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        # Enable right click on page
        web.page().mainFrame().evaluateJavaScript("var debug=true;")


    # Html and js
    Pyjs = Pyjs()
    Pyjs.debug = debug
    html = QUrl("file://" + os.getcwd() + "/index.html#/")

    # Load html and js
    web.load(html)
    web.page().mainFrame().addToJavaScriptWindowObject("Pyjs", Pyjs)

    # Show webview
    web.show()

    # Quit application
    ret = app.exec_()
    # Execute before quit
    Pyjs.debug = True
    Pyjs.getApps()
    sys.exit(ret)