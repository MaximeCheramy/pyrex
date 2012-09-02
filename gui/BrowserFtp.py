import PyQt4.uic
from Tools import convert_size_str
from PyQt4.QtGui import QWidget, QTableWidgetItem
from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QFtp

class BrowserFtp(QWidget):

    def __init__(self, url, parent=None):
        super(BrowserFtp, self).__init__(parent)

        PyQt4.uic.loadUi('ui/browser.ui', self)

        self._url = QUrl(url)
        self.ftp = QFtp(self)

        self.ftp.commandFinished.connect(self.command_finished)
        self.ftp.listInfo.connect(self.list_info)

        self.ftp.connectToHost(self._url.host(), self._url.port(21))
        self.ftp.login()

        if self._url.path():
            self.ftp.cd(self._url.path())

    def activated(self, row, col):
        print row, col

    def list_info(self, url_info):
        rows = self.list_table.rowCount()
        self.list_table.insertRow(rows)
        self.list_table.setItem(rows, 0, QTableWidgetItem(url_info.name()))
        self.list_table.setItem(rows, 1, QTableWidgetItem(convert_size_str(url_info.size())))
        self.list_table.setItem(rows, 2, QTableWidgetItem(url_info.lastModified().toString('dd/MM/yyyy')))

    def command_finished(self, _, err):
        if self.ftp.currentCommand() == QFtp.Login:
            self.ftp.list()

