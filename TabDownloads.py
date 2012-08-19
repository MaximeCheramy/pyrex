#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem

from ftp import Ftp

class Download(object):
    def __init__(self, file_share, local_path):
        self._file_share = file_share
        self._local_path = local_path

    @property
    def file_share(self):
        return self._file_share

    @property
    def local_path(self):
        return self._local_path

    @property
    def progress(self):
        return '0.0'

    @property
    def state(self):
        return u'Terminé'

    def start_download(self):
        self.ftp = Ftp(QUrl(self._file_share.url), self._local_path, self.update_progress)

    def update_progress(self, readBytes, totalBytes):
        print "%d / %d" % (readBytes, totalBytes)


class TabDownloads(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('telechargements.ui', self)

        TabDownloads.instance = self
        self.downloads = []

    def add_download(self, download):
        rows = self.downloads_table.rowCount()
        self.downloads_table.insertRow(rows)
        self.downloads_table.setItem(rows, 0, QTableWidgetItem(download.file_share.name))
        self.downloads_table.setItem(rows, 1, QTableWidgetItem(download.progress))
        self.downloads_table.setItem(rows, 2, QTableWidgetItem(download.state))
        download.start_download()
        self.downloads.append(download)
