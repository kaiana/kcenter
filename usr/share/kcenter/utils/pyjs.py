#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import QObject, pyqtSlot
from utils import kinfoservices
import json
import subprocess


class Pyjs(QObject):

    @pyqtSlot(result=str)
    def getApps(self):
        items = kinfoservices.getservices()
        return json.dumps(items)

    @pyqtSlot(str, result=str)
    def run_kde(self, cmd):
        subprocess.Popen(cmd, shell=True, stdin=None, stdout=subprocess.PIPE, stderr=subprocess.PIPE)