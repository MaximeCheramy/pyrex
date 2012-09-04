#!/usr/bin/python
# coding=utf-8

import os
import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem

from downloads import AnalyseDownloads

from Tools import convert_speed_str

class TabDownloads(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        # Load de l'UI
        PyQt4.uic.loadUi('ui/downloads.ui', self)
        # Vars 
        TabDownloads.instance = self
        self.downloads = []
        # Init
        self.load_downloads()

    def load_downloads(self):
        import xml.sax
        parser = xml.sax.make_parser()
        parser.setContentHandler(AnalyseDownloads(self.add_downloads))
        for line in open(os.path.expanduser("~") + '/.rex/downloads.xml'):
            parser.feed(line)

    def add_download(self, download):
        rows = self.downloads_table.rowCount()
        self.downloads_table.insertRow(rows)
        self.downloads_table.setItem(rows, 0, QTableWidgetItem(download.file_share.name))
        self.downloads_table.setItem(rows, 1, QTableWidgetItem(download.get_progress()))
        self.downloads_table.setItem(rows, 2, QTableWidgetItem(download.state))
        self.downloads_table.setItem(rows, 3, QTableWidgetItem("0 ko/s"))
        self.downloads_table.setItem(rows, 5, QTableWidgetItem(download.date.strftime('%d/%m/%y')))
        self.downloads.append(download)
        # Signaux
        download.progressModified.connect(self.update_progress)
        download.stateChanged.connect(self.update_state)
        download.downloadFinished.connect(self.download_finished)
        download.speedModified.connect(self.update_speed)

    def add_downloads(self, downloads):
        for download in downloads:
          self.add_download(download)
          
    def update_progress(self, download):
        item = self.downloads_table.findItems(download.file_share.name, Qt.MatchExactly)[0]
        row = self.downloads_table.row(item)
        self.downloads_table.item(row, 1).setText(download.get_progress())

    def update_speed(self, download):
        item = self.downloads_table.findItems(download.file_share.name, Qt.MatchExactly)[0]
        row = self.downloads_table.row(item)
        self.downloads_table.item(row, 3).setText(convert_speed_str(download.speed))
        
    def update_state(self, download):
        item = self.downloads_table.findItems(download.file_share.name, Qt.MatchExactly)[0]
        row = self.downloads_table.row(item)
        self.downloads_table.item(row, 2).setText(download.state)
        
    def download_finished(self, download):
        if download.read_bytes == download.file_share.size:
            item = self.downloads_table.findItems(download.file_share.name, Qt.MatchExactly)[0]
            row = self.downloads_table.row(item)
            self.downloads_table.item(row, 2).setText("Finished!")
        else:
            print "Erreur dans le téléchargement"
            item = self.downloads_table.findItems(download.file_share.name, Qt.MatchExactly)[0]
            row = self.downloads_table.row(item)
            self.downloads_table.item(row, 2).setText("Error :(")
