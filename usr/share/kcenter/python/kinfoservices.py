#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess
import gettext
from xdg.DesktopEntry import *
from xdg.IconTheme import *
from collections import OrderedDict
import re

# get translations
gettext.install("kcenter", "/usr/share/locale/kcenter")

def getservices():

    # get list of desktop files for kde
    command = "grep -l kcmshell4 /usr/share/kde4/services/*.desktop"
    files = subprocess.getoutput(command).splitlines()

    # get list of desktop files for big
    command = "ls -d -1 " + os.getcwd() + "/includes/*.desktop"
    files += subprocess.getoutput(command).splitlines()

    # get current theme
    command = "kreadconfig --group 'Icons' --key 'Theme'"
    theme = subprocess.getoutput(command)

    # output
    output = {}

    # Map category
    category_types = {
        "X-KDE-settings-accessibility": _("DESKTOP"),
        "X-KDE-settings-components": _("DESKTOP"),
        "X-KDE-settings-desktop": _("DESKTOP"),
        "X-KDE-settings-looknfeel": _("LOOK AND FEEL"),
        "X-KDE-settings-network": _("NETWORK AND CONNECTIVITY"),
        "X-KDE-settings-webbrowsing": _("NETWORK AND CONNECTIVITY"),
        "X-KDE-settings-peripherals": _("HARDWARE"),
        "X-KDE-settings-hardware": _("HARDWARE"),
        "X-KDE-settings-power": _("SYSTEM"),
        "X-KDE-settings-security": _("SECURITY"),
        "X-KDE-settings-sound": _("HARDWARE"),
        "X-KDE-settings-system": _("SYSTEM"),
        "X-KDE-settings-bluetooth": _("NETWORK AND CONNECTIVITY"),
        "X-KDE-settings-system-administration": _("SYSTEM"),
        "X-KDE-settings-user_manager": _("SYSTEM"),
        "X-KDE-information": _("INFORMATIONS OF SYSTEM")
    }


    # extra configurations
    apps_remove = open(os.getcwd() + "/conf/remove.conf").read().splitlines()
    apps_category = open(os.getcwd() + "/conf/category.conf").read().splitlines()

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
        category = None

        # fix error on get icon path
        if icon == "None":
            icon = str(getIconPath("preferences-system", theme=theme, size=32))

        # check recategorize
        regex=re.compile(filename + "=*")
        #result=[m.group(0) for l in apps_category for m in [regex.search(l)] if m]
        for line in apps_category:
            if regex.search(line):
                category = line.split("=")[1]

        if category is None:
            # get categories from file
            file_categories = entry.getCategories()

            # get category
            for elem in file_categories:
                category = elem

            #if filename == 'icons':
            #    print(file)

            # define to execute
            if "/usr/share/kde4" not in file:
                execute = entry.getExec()
                category = _(category)
            else:

                # remove applications
                if filename in apps_remove:
                    continue

                execute = "kcmshell4 " + str(filename)

                # get current category from file
                try:
                    if category is None:
                        raise Exception()
                    category = category_types[category]
                except:
                    category = _("Others Configurations")

        # convert to upper
        category = category.upper()

        # fill array service
        if category not in output:
            output[category] = []

        output[category].append({
            "execute": execute,
            "comment": comment,
            "icon": icon,
            "name": name
        })

    output = OrderedDict(sorted(output.items()))
    return output
