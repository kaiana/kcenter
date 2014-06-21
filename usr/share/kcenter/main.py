#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import gettext
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebKit import QWebSettings
from PyQt5.QtWebKitWidgets import QWebView
from PyQt5.QtCore import QUrl
from utils.pyjs import Pyjs

# get translations
gettext.install("kcenter", "/usr/share/locale/kcenter")

if __name__ == "__main__":
    # Create application QT and create WebView
    app = QApplication([])
    web = QWebView()

    # Set Title
    web.setWindowTitle(_("Kaiana Control Panel"))

    # Configurations: Center Window and Enable extra tools for developers
    web.move(app.desktop().screen().rect().center() - web.rect().center())
    web.page().settings().setAttribute(
        QWebSettings.DeveloperExtrasEnabled,
        True
    )

    # Html and js
    Pyjs = Pyjs()
    html = QUrl("file://" + os.getcwd() + "/index.html#/")

    # Load html and js
    web.load(html)
    web.page().mainFrame().addToJavaScriptWindowObject("Pyjs", Pyjs)

    # Show webview
    web.show()

    # Quit application
    ret = app.exec_()
    # Execute before quit
    #Pyjs.getApps(cache=False)
    sys.exit(ret)