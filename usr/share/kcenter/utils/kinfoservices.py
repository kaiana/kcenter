#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import gettext
from xdg.DesktopEntry import *
from xdg.IconTheme import *
from collections import OrderedDict

# get translations
gettext.install("kcenter", "/usr/share/locale/kcenter")


def getservices():

    # get list of desktop files
    command = "grep -l kcmshell4 /usr/share/kde4/services/*.desktop"
    files = subprocess.getoutput(command).splitlines()

    # get current theme
    command = "kreadconfig --group 'Icons' --key 'Theme'"
    theme = subprocess.getoutput(command)

    services = {}

    # Map category
    category_types = {
        "X-KDE-settings-accessibility": _("Desktop"),
        "X-KDE-settings-components": _("Desktop"),
        "X-KDE-settings-desktop": _("Desktop"),
        "X-KDE-settings-looknfeel": _("Look and Feel"),
        "X-KDE-settings-network": _("Network and Connectivity"),
        "X-KDE-settings-webbrowsing": _("Network and Connectivity"),
        "X-KDE-settings-peripherals": _("Hardware"),
        "X-KDE-settings-hardware": _("Hardware"),
        "X-KDE-settings-power": _("System"),
        "X-KDE-settings-security": _("Security"),
        "X-KDE-settings-sound": _("Hardware"),
        "X-KDE-settings-system": _("System"),
        "X-KDE-settings-bluetooth": _("Network and Connectivity"),
        "X-KDE-settings-system-administration": _("System"),
        "X-KDE-settings-user_manager": _("System"),
        "X-KDE-information": _("Informations of System")
    }

    # get informations from files
    for file in files:

        entry = DesktopEntry()

        # parse file
        try:
            entry.parse(file)
        except:
            continue

        # data from file
        name = entry.getName()
        comment = entry.getComment()
        icon = str(getIconPath(entry.getIcon(), theme=theme, size=32))
        filename = os.path.splitext(os.path.basename(file))[0]

        # fix error on get icon path

        if icon == "None":
            icon = os.getcwd() + "/static/images/applications.png"
            print(icon)

        # get categories from file
        file_categories = entry.getCategories()

        # get category reference kde
        category = None
        for elem in file_categories:
                category = elem

        # get current category from file
        try:

            if category is None:
                raise Exception()

            category = category_types[category]

        except:
            category = _("Others Configurations")

        # fill array service
        if category not in services:
            services[category] = []

        services[category].append({
            "filename": filename,
            "comment": comment,
            "icon": icon,
            "name": name
        })

    services = OrderedDict(sorted(services.items()))
    return services


#print(getservices())
#getservices()
