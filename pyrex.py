#!/usr/bin/python
# coding=utf-8

import os
import sys
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import *

from gui import MainWindow
from configuration import Configuration

if __name__ == '__main__':
    app = QApplication([])
    
    # Translation process
    locale = QLocale.system().name()
    qtTranslator = QTranslator()
    if qtTranslator.load("qt_" + locale):
        app.installTranslator(qtTranslator)
    buttonTranslator = QTranslator()
    if buttonTranslator.load("qt_" + locale, QLibraryInfo.location(QLibraryInfo.TranslationsPath)) :
        app.installTranslator(buttonTranslator)
    appTranslator = QTranslator()
    if appTranslator.load("pyrex_" + locale):
        app.installTranslator(appTranslator)
    
    # On vérifie que le dossier ~/.pyrex existe, si non on le créé
    if not os.path.isdir(os.path.expanduser("~/.pyrex/")):
        try:
            print("Création du dossier ~/.pyrex")
            os.mkdir(os.path.expanduser("~/.pyrex/"))
        except OSError:
            print("Erreur : le dossier n'a pas pu être créé")
            
    print("On loade la config du GUI")
    Configuration.load_config()

    window = MainWindow()
    window.show()
    
    app.exec_()
