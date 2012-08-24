#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

from search import Search

class TabAdvSearch(QWidget):
    instance = None

    def __init__(self, search_tab, parent=None):
        QWidget.__init__(self, parent)
        self.search_tab = search_tab
        PyQt4.uic.loadUi('ui/adv_search.ui', self)
    
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
        extensions = ""
        extensions += str(self.combo_type_fichier.currentText())
        if extensions == "Tous":
            extensions = None
        elif extensions == "Vidéos":
            extensions = "avi,mpg,mpeg,divx,mkv,mov,wmv,mp4,flv,ogm,m4v,rm,rmvb,mts,m2ts"
        elif extensions == "Musiques":
            extensions = "mp3,wma,ogg,m4a,aac,flac,wv,wav,ra,kfn,kar,mid"
        elif extensions == "Images":
            extensions = "jpg,jpeg,png,bmp,gif"
        elif extensions == "Documents":
            extensions = "txt,pdf,rtf,doc,docx,odt,xls,xlsx,ods,ppt,pps,pptx,odp"
        elif extensions == "Archives":
            extensions = "tar,gz,bz2,rar,zip,iso,7z,mds,nrg,cue"
        extensions += str(self.ext_edit.text()).replace(' ','').replace('/',',')
        # Taille min
        sizeinf = int(self.lineEdit_4.text())
        # Taille max
        sizesup = int(self.lineEdit_6.text())
        # TODO: Adresses IP et Date
        # On recherche
        if len(query) > 1:
            search = Search(query, protocol, Type, extensions, sizeinf, sizesup)
            search_tab.add_search(search)

