#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QMainWindow, QTabWidget, QSystemTrayIcon, QIcon, QMenu, QAction

import images
from TabSearch import TabSearch
from TabPeers import TabPeers
from TabDownloads import TabDownloads
from TabOptions import TabOptions
from TabShares import TabShares
from TabAdvSearch import TabAdvSearch
from TabInformations import TabInformations
from configuration import Configuration

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        PyQt4.uic.loadUi('ui/pyrex.ui', self)

        # Icon:
        self.setWindowIcon(QIcon("res/rex_18.png"))

        # Tray Icon:
        self.trayIcon = QSystemTrayIcon(QIcon("res/rex_18.png"), self)
        trayMenu = QMenu()
        self.actionQuit = QAction("Quitter", trayMenu)
        self.actionQuit.triggered.connect(self.close)
        trayMenu.addAction(self.actionQuit)
        self.trayIcon.setContextMenu(trayMenu)
        #self.trayIcon.show()

        QObject.connect(self.trayIcon, SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.icon_activated)
 
        # Tabs:
        self.tabs = QTabWidget()
        QObject.connect(self.tabs, SIGNAL('currentChanged(int)'), self.change_tab)

        self.search = TabSearch(self.tabs)
        self.adv_search = TabAdvSearch(self.search, self.tabs)
        self.peers = TabPeers(self.search, self.tabs)
        self.downloads = TabDownloads(self.tabs)
        self.options = TabOptions(self.tabs)
        self.shares = TabShares(self.tabs)
        self.informations = TabInformations(self.tabs)

        self.tabs.insertTab(0, self.search, u"Recherches")
        self.tabs.insertTab(1, self.adv_search, u"Recherche avancée")
        self.tabs.insertTab(2, self.downloads, u"Téléchargements")
        self.tabs.insertTab(3, self.peers, u"Utilisateurs")
        self.tabs.insertTab(4, self.options, u'Options')
        self.tabs.insertTab(5, self.shares, u'Mes partages')
        self.tabs.insertTab(6, self.informations, u'Informations')
        
        self.setCentralWidget(self.tabs)

    def change_tab(self, tab):
        if tab == 3:
            self.peers.update_peers()
        elif tab == 4:
            self.options.update_conf()
        elif tab == 5:
            self.shares.update_sharedirs()
        elif tab == 6:
            self.informations.update_informations()

    def closeEvent(self, event):
        if not self.trayIcon.isVisible() and Configuration.icon:
            self.trayIcon.show()
            self.hide()
            event.ignore()
        else:
            event.accept()
   
    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.isMinimized():
                self.trayIcon.show()
                self.hide()
 
    def icon_activated(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
                self.activateWindow()
                self.show()
                self.trayIcon.hide()
