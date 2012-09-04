#!/usr/bin/python
# coding=utf-8

import os
import subprocess
import sys
import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QTableWidgetItem, QMenu, QApplication

from downloads import AnalyseDownloads

from Tools import convert_speed_str

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, string, download):
        QTableWidgetItem.__init__(self, string)
        self.download = download

class TabDownloads(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        # Load de l'UI
        PyQt4.uic.loadUi('ui/downloads.ui', self)
        # Vars 
        TabDownloads.instance = self
        self.downloads        = []
        self.pos              = None
        # On autorise la creation de menu contextuel
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # Signaux
        self.customContextMenuRequested.connect(self.contextMenu)
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
        self.downloads_table.setItem(rows, 0, MyQTableWidgetItem(download.file_share.name, download))
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
            
    def contextMenu(self, pos):
        self.pos = pos
        menu = QMenu()
        # Actions 
        forceAction         = menu.addAction("Forcer la reprise")
        continueAction      = menu.addAction("Reprise")
        pauseAction         = menu.addAction("Pause")
        openAction          = menu.addAction("Ouvrir le dossier")
        supprListeAction    = menu.addAction("Supprimer de la liste")
        supprDiskAction     = menu.addAction("Supprimer de la liste et du disque")
        copyAction          = menu.addAction("Copier l'URL")
        searchAction        = menu.addAction("Rechercher des fichiers similaires")
        # Signaux
        self.connect(forceAction, SIGNAL('triggered()'), self.force_Action)
        self.connect(continueAction, SIGNAL('triggered()'), self.continue_Action)
        self.connect(pauseAction, SIGNAL('triggered()'), self.pause_Action)
        self.connect(openAction, SIGNAL('triggered()'), self.open_Action)
        self.connect(supprListeAction, SIGNAL('triggered()'), self.suppr_liste_Action)
        self.connect(supprDiskAction, SIGNAL('triggered()'), self.suppr_disk_Action)
        self.connect(copyAction, SIGNAL('triggered()'), self.copy_Action)
        self.connect(searchAction, SIGNAL('triggered()'), self.search_Action)
        # On affiche le menu
        menu.exec_(self.mapToGlobal(pos))
      
    def getDownload(self):
        row = self.downloads_table.currentRow()
        return self.downloads_table.item(row, 0).download
          
    def force_Action(self):
        print "TODO"
        
    def continue_Action(self):
        print "TODO"
        
    def pause_Action(self):
        print "TODO"
        
    def open_Action(self):
        download = self.getDownload()
        if sys.platform == 'linux2':
            subprocess.check_call(['gnome-open', download.local_path.strip(download.file_share.name)])
        elif sys.platform == 'windows':
            subprocess.check_call(['explorer', download.local_path.strip(download.file_share.name)])
        
    def suppr_liste_Action(self):
        print "TODO"
        
    def suppr_disk_Action(self):
        print "TODO"
        
    def copy_Action(self):
        pressPaper = QApplication.clipboard()
        pressPaper.setText(self.getDownload().local_path)
        
    def search_Action(self):
        print "TODO"
