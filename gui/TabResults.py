import PyQt4.uic
from PyQt4.QtGui import QWidget, QTabWidget, QTableWidgetItem
from PyQt4.QtCore import *

from downloads import Download
from TabDownloads import TabDownloads

from datetime import date

class MyQTableWidgetItem(QTableWidgetItem):
    def __init__(self, string, share):
        QTableWidgetItem.__init__(self, string)
        self.share = share


class TabResults(QWidget):
    resultsReceived = pyqtSignal(list)

    def __init__(self, search, parent=None):
        super(TabResults, self).__init__(parent)

        PyQt4.uic.loadUi('ui/tabresult.ui', self)

        self.resultsReceived.connect(self.add_results)

        search.do_search(self._send_signal_results)

    def _send_signal_results(self, results):
        self.resultsReceived.emit(results)

    def _add_share(self, share):
        rows = self.table_results.rowCount()
        self.table_results.insertRow(rows)
        self.table_results.setItem(rows, 0, MyQTableWidgetItem(share.name, share))
        self.table_results.setItem(rows, 1, QTableWidgetItem(share.str_size))
        self.table_results.setItem(rows, 2, QTableWidgetItem(share.nickname))
        self.table_results.setItem(rows, 3, QTableWidgetItem("%.2f" % share.score))
        self.table_results.setItem(rows, 4, QTableWidgetItem(share.str_last_modified))
        self.table_results.setItem(rows, 5, QTableWidgetItem(share.protocol))

    def add_results(self, results):
        for share in results:
            self._add_share(share)

    def double_clicked(self, row, col):
        self.download(self.table_results.item(row, 0).share)

    def download(self, share):
        dl = Download.get_download(share, share.name, date.today())
        TabDownloads.instance.add_download(dl)
        dl.start_download()

class TabsResults(QTabWidget):
    def __init__(self, parent):
        QTabWidget.__init__(self, parent)
        self.setTabsClosable(True)
        self.setMovable(True)
        QObject.connect(self, SIGNAL('tabCloseRequested(int)'), self.close_tab)
        
    def close_tab(self, index):
        self.removeTab(index)

