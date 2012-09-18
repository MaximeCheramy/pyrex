#!/usr/bin/python
# coding=utf-8

import os

from PyQt4.QtGui import QApplication
from PyQt4 import QtCore

from gui import MainWindow
from configuration import Configuration

if __name__ == '__main__':
    app = QApplication([])
    
    # Translation process
    locale = QtCore.QLocale.system().name()
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + locale):
        app.installTranslator(qtTranslator)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("pyrex_" + locale):
        app.installTranslator(appTranslator)
    
    # On vérifie que le dossier ~/.pyrex existe, si non on le créé
    if not os.path.isdir(os.path.expanduser("~/.pyrex/")):
        try:
            print "Création du dossier ~/.pyrex"
            os.mkdir(os.path.expanduser("~/.pyrex/"))
        except OSError:
            print "Erreur : le dossier n'a pas pu être créé"
            
    print "On loade la config du GUI"
    Configuration.load_config()

    window = MainWindow()
    window.show()
    
    app.exec_()
