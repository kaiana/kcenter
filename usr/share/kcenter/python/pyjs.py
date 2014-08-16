#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSlot
from python import kinfoservices
import json
import subprocess
import os


class Pyjs(QObject):

    debug = False

    @pyqtSlot(result=str)
    def getApps(self):
        filename = os.getenv("HOME") + "/.kcenter/getApps"
        items = None

        try:
            if not self.debug:
                if os.path.exists(filename):
                    items = open(filename, 'r').read()
                else:
                    raise Exception()
            else:
                raise Exception()

        except:
            items = json.dumps(kinfoservices.getservices())

            if not os.path.exists(os.path.dirname(filename)):
                os.makedirs(os.path.dirname(filename))

            with open(filename, "w") as f:
                f.write(items)

        return items



    @pyqtSlot(str, result=str)
    def cmd(self, cmd):
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
