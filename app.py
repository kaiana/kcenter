#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from project import app

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 2222))
    app.run('127.0.0.1', port=port)
