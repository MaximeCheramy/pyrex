#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

class TabAdvSearch(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('ui/adv_search.ui', self)

