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
from python.pyjs import Pyjs
from configparser import ConfigParser

# get translations
gettext.bindtextdomain('kcenter', os.getcwd() + "/../locale")
gettext.textdomain('kcenter')
_ = gettext.gettext

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


    # Get dimensions from config file
    config = ConfigParser()
    configFile = None
    configFilePath = os.getenv("HOME") + "/.kcenter/conf"
    width, height = 800, 600
    x = y = None
    if os.path.exists(configFilePath):
        config.read(configFilePath)
        width = config.get('window','width') if config.has_option('window','width') else width
        height = config.get('window','height') if config.has_option('window','height') else height
        x = config.get('window','x') if config.has_option('window','x') else x
        y = config.get('window','y') if config.has_option('window','y') else y

    else:
        basedir = os.path.dirname(configFilePath)
        if not os.path.exists(basedir):
            os.makedirs(basedir)
        config.add_section('window')


    # Define geometry
    web.resize(int(width), int(height))

    # center window
    if(x is None or y is None):
        web.move(app.desktop().screen().rect().center() - web.rect().center())
    else:
        web.move(int(x), int(y))


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
    html = QUrl("file://" + os.getcwd() + "/static/index.html")

    # Load html and js
    web.load(html)
    web.page().mainFrame().addToJavaScriptWindowObject("Pyjs", Pyjs)

    # Show webview
    web.show()

    # Quit application
    ret = app.exec_()
    ### Execute before quit ###

    # Save window config
    config.set('window', 'width', str(web.frameGeometry().width()))
    config.set('window', 'height', str(web.frameGeometry().height()))
    config.set('window', 'x', str(web.geometry().x()))
    config.set('window', 'y', str(web.geometry().y()))
    with open(configFilePath, 'w') as file:
        config.write(file)

    # Save cache for apps
    Pyjs.debug = True
    Pyjs.getApps()

    ### Execute before quit ###
    sys.exit(ret)