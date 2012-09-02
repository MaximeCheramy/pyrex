#!/usr/bin/python
# coding=utf-8

import os
import time
import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem

from downloads import AnalyseDownloads

class TabDownloads(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        # Load de l'UI
        PyQt4.uic.loadUi('ui/downloads.ui', self)
        # Vars 
        TabDownloads.instance = self
        self.downloads = []
        self.pas       = 100
        self.count     = 0
        self.last_size = 0
        self.last_time = time.time()
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

    def add_downloads(self, downloads):
        for download in downloads:
          self.add_download(download)
          
    def update_progress(self, download):
        item = self.downloads_table.findItems(download.file_share.name, Qt.MatchExactly)[0]
        row = self.downloads_table.row(item)
        self.downloads_table.item(row, 1).setText(download.get_progress())
        # Pour la vitesse instantannée
        if self.count == self.pas:
            progression = download.read_bytes - self.last_size
            tps = time.time() - self.last_time
            progression = progression/tps
            if progression > 1024*1024:
                s_progression = "{0:.1f} {1}".format(progression/(1024*1024), "Mio/s")
                self.pas = 175
            elif progression > 1024:
                s_progression = "{0:.1f} {1}".format(progression/1024, "kio/s")
                if progression/1024 > 500:
                    self.pas = 125
                elif progression/1024 > 250:
                    self.pas = 100
                elif progression/1024 > 100:
                    self.pas = 50
                elif progression/1024 > 50:
                    self.pas = 25
                else:
                    self.pas = 10
            elif progression > 0:
                s_progression = "{0:.1f} {1}".format(progression, "io/s")
                self.pas = 1
            else:
                s_progression = "0 ko/s"
                self.pas = 1
            self.downloads_table.item(row, 3).setText(s_progression)
            self.last_time = time.time()
            self.last_size = download.read_bytes
            self.count = 0
        else:
            self.count += 1
        
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
