import PyQt4.uic
from datetime import date
from configuration import Configuration
from TabDownloads import TabDownloads
from downloads import Download
from Share import FileShare, DirectoryShare
from Tools import convert_size_str
from PyQt4.QtGui import QWidget, QTableWidgetItem
from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QFtp

class SizeItem(QTableWidgetItem):
    def __init__(self, is_dir, size):
        if is_dir:
            super(SizeItem, self).__init__('Dossier')
        else:
            super(SizeItem, self).__init__(convert_size_str(size))

        self.size = size


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
        name = self.list_table.item(row, 0).text()
        if self.list_table.item(row, 1).text():
            size = self.list_table.item(row, 1).size

            share = FileShare(name, self._url.host(), self._url.port(21), self._url.path(), 'FTP', size, 0, '')
            dl = Download.get_download(share, Configuration.save_dir + "/" + share.name, date.today())
            TabDownloads.instance.add_download(dl)
            dl.start_download()
        else:
            share = DirectoryShare(name, self._url.host(), self._url.port(21), self._url.path(), 'FTP', 0, '')
            self._url = QUrl(share.url)
            self.ftp.cd(self._url.path())

    def list_info(self, url_info):
        rows = self.list_table.rowCount()
        self.list_table.insertRow(rows)
        self.list_table.setItem(rows, 0, QTableWidgetItem(url_info.name()))
        if url_info.isDir():
            self.list_table.setItem(rows, 1, SizeItem(True, 0))
        else:
            self.list_table.setItem(rows, 1, SizeItem(False, url_info.size()))
        self.list_table.setItem(rows, 2, QTableWidgetItem(url_info.lastModified().toString('dd/MM/yyyy')))

    def command_finished(self, _, err):
        if self.ftp.currentCommand() == QFtp.Cd:
            while self.list_table.rowCount() > 0:
                self.list_table.removeRow(0)
            self.ftp.list()

