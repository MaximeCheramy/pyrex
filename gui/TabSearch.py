#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget

from search import Search

from TabResults import TabResults, TabsResults

class TabSearch(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)

        PyQt4.uic.loadUi('ui/search.ui', self)

        self.tabs_results = TabsResults(self.widget_searches)
        self.widget_searches.layout().addWidget(self.tabs_results)

    def search(self):
        query = str(self.search_edit.text())
        if len(query) > 1:
            self.add_search(Search(query))

    def add_search(self, search):
        tab_result = TabResults(search, self.tabs_results)
        self.tabs_results.addTab(tab_result, search.query)
        self.tabs_results.setCurrentWidget(tab_result)
