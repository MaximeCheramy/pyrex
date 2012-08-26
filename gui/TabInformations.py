#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

from stats import StatisticsGet
from version import VersionGet

class TabInformations(QWidget):
    statsReceived = pyqtSignal(object)
    versionReceived = pyqtSignal(object)
    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('ui/informations.ui', self)

        self.statsReceived.connect(self.set_statistics)
        self.versionReceived.connect(self.set_version)

    def update_informations(self):
        self.stats_get = StatisticsGet(self.statsReceived.emit)
        self.stats_get.do_get()

        self.version_get = VersionGet()
        self.version_get.do_get(self.versionReceived.emit)

    def set_statistics(self, stats):
        txt = u"Utilisateurs connectés : %d\n" % stats.users
        txt += u"Taille de vos fichiers dans la base : %s\n" % stats.shares_size_mine_str
        txt += u"Taille des fichiers dans la base : %s" % stats.shares_size_total_str
        self.statistics_label.setText(txt)

    def set_version(self, version):
        txt = "%s version %d.%d.%d\n" % \
           (version.name, version.major, version.minor, version.minor_minor)
        txt += "PyRex version 0.0.1"
        self.version_label.setText(txt)
