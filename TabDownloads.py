#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem

from downloads import AnalyseDownloads

class TabDownloads(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('telechargements.ui', self)

        TabDownloads.instance = self
        self.downloads = []

        self.load_downloads()

    def load_downloads(self):
        import xml.sax
        parser = xml.sax.make_parser()
        parser.setContentHandler(AnalyseDownloads(self.add_downloads))
        for line in open('/home/max/.rex/downloads.xml'):
          parser.feed(line)

    def add_download(self, download):
        rows = self.downloads_table.rowCount()
        self.downloads_table.insertRow(rows)
        self.downloads_table.setItem(rows, 0, QTableWidgetItem(download.file_share.name))
        self.downloads_table.setItem(rows, 1, QTableWidgetItem(download.get_progress()))
        self.downloads_table.setItem(rows, 2, QTableWidgetItem(download.state))
        self.downloads_table.setItem(rows, 5, QTableWidgetItem(download.date.strftime('%d/%m/%y')))
        self.downloads.append(download)

    def add_downloads(self, downloads):
        for download in downloads:
          self.add_download(download)
