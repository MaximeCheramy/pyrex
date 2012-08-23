#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

from search import Search
from TabResults import TabResults, TabsResults

class TabAdvSearch(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('ui/adv_search.ui', self)
	
    # TODO : connecter adv_search avec le bouton "rechercher"
    def adv_search(self):
	# Texte de la recherche
        query = str(self.search_edit2.text())
	# Protocole de la recherche (FTP, SMB)
	protocol = str(self.combo_type_partage.currentText())
	if protocol == "FTP + SMB":
		protocol = None
	elif protocol == "FTP uniquement":
		protocol = "FTP"
	elif protocol == "SMB uniquement":
		protocol = "SMB"
	# Type de recherche (fichiers, dossiers)
	Type = str(self.combo_fichier_dossier.currentText())
	if Type == "Fichiers et dossiers":
		Type = None
	elif Type == "Fichiers uniquement":
		Type = "FILE"
	elif Type == "Dossiers uniquement":
		Type = "DIRECTORY"
	# Extensions de la recherche
	extensions = []
	extensions += str(self.combo_type_fichier.currentText())
	if extensions[0] == "Tous":
		extensions = []
	elif extensions[0] == "Vidéos":
		extensions[0] = "avi,mov,mpeg"
	elif extensions[0] == "Musiques":
		extensions[0] = "mp3,wav,ogg,ac3"
	elif extensions[0] == "Images":
		extensions[0] = "jpeg,jpg,gif,png"
	elif extensions[0] == "Documents":
		extensions[0] = "bat,doc,xls,exe,iso,htm,html,pdf,ppt,zip"
	elif extensions[0] == "Archives":
		extensions[0] = "zip,tar.gz,tar,bz2"
	extensions += str(self.ext_edit.text())
	# Taille min
	# TODO
	# Taille max
	# TODO
	if len(query) > 1:
            search = Search(query) #TBM
            tab_result = TabResults(search, parent=self.tabs_results)
            self.tabs_results.addTab(tab_result, query)


