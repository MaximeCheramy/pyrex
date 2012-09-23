import PyQt4.uic
from datetime import date
from configuration import Configuration
from TabDownloads import TabDownloads
from downloads import Download
from Share import FileShare
from Tools import convert_size_str
from PyQt4.QtGui import QWidget, QTableWidgetItem
from PyQt4.QtCore import QUrl
from PyQt4.QtNetwork import QFtp

class SizeItem(QTableWidgetItem):
    def __init__(self, is_dir, size):
        if is_dir:
            super(SizeItem, self).__init__('dossier')
        else:
            super(SizeItem, self).__init__(convert_size_str(size))

        self.size = size


class BrowserFtp(QWidget):
    def __init__(self, url, tabs, tab_download, parent=None):
        super(BrowserFtp, self).__init__(parent)
        # Load de l'UI
        PyQt4.uic.loadUi('ui/browser.ui', self)
        # Affichage custom
        #self.list_table.setStyleSheet(\
        #        "QTableView::item{ \
        #         border-right-style:solid; \
        #         border-width:0.5; \
        #         border-color: #9B9B9B; \
        #         }")
        self.list_table.horizontalHeader().setStretchLastSection(True)
        self.list_table.resizeColumnsToContents()
        # Init FTP
        self._url = QUrl(url)
        self.ftp = QFtp(self)
        # Signaux
        self.ftp.commandFinished.connect(self.command_finished)
        self.ftp.listInfo.connect(self.list_info)
        # Load FTP
        self.ftp.connectToHost(self._url.host(), self._url.port(21))
        self.ftp.login()
        # Vars
        self.tabs           = tabs
        self.tab_download   = tab_download
        self._cmd_prev_next = False
        self._history       = []
        self._cur_pos       = 0
        self._change_dir('.')

    def _address_changed(self):
        self._change_dir(self.address_bar.text())

    def _cd_parent_dir(self):
        if self._url.path() != '/':
            self._change_dir('..')

    def _prev(self):
        if self._cur_pos > 1:
            self._cur_pos -= 1
            self._next_url = self._history[self._cur_pos - 1]
            self._cmd_prev_next = True
            self.ftp.cd(self._next_url.path())
            self.next_button.setEnabled(True)
            self.prev_button.setEnabled(self._cur_pos > 1)

    def _next(self):
        if self._cur_pos < len(self._history):
            self._next_url = self._history[self._cur_pos]
            self._cmd_prev_next = True
            self.ftp.cd(self._next_url.path())
            self._cur_pos += 1
            self.next_button.setEnabled(self._cur_pos < len(self._history))
            self.prev_button.setEnabled(self._cur_pos > 1)

    def _change_dir(self, rel_path):
        url = self._url.resolved(QUrl(rel_path))
        if url != rel_path:
            self._cmd_prev_next = False
            self._next_url = url
            self.ftp.cd(url.path())

    def activated(self, row, col):
        name = self.list_table.item(row, 0).text()
        size = self.list_table.item(row, 1).size
        if size:
            share = FileShare(unicode(name.toUtf8(), 'utf-8'), unicode(self._url.host().toUtf8(), 'utf-8'), self._url.port(21), unicode(self._url.path().toUtf8(), 'utf-8'), 'FTP', size, 0, '')
            dl = Download.get_download(share, Configuration.save_dir + "/" + share.name, date.today())
            TabDownloads.instance.add_download(dl)
            dl.start_download()
            self.tabs.setCurrentWidget(self.tab_download)
        else:
            self._change_dir(name)

    def list_info(self, url_info):
        if url_info.size() > 0 or url_info.isDir():
            rows = self.list_table.rowCount()
            self.list_table.insertRow(rows)
            if url_info.isDir():
                self.list_table.setItem(rows, 0, QTableWidgetItem(url_info.name() + '/'))
                self.list_table.setItem(rows, 1, SizeItem(True, 0))
            else:
                self.list_table.setItem(rows, 0, QTableWidgetItem(url_info.name()))
                self.list_table.setItem(rows, 1, SizeItem(False, url_info.size()))
            self.list_table.setItem(rows, 2, QTableWidgetItem(url_info.lastModified().toString('dd/MM/yyyy')))

    def command_finished(self, _, err):
        if self.ftp.currentCommand() == QFtp.Cd:
            if err:
                self.address_bar.setText(self._url.path())
            else:
                if not self._cmd_prev_next:
                    self._history = self._history[:self._cur_pos]
                    self._history.append(self._next_url)
                    self._cur_pos += 1
                    self.prev_button.setEnabled(self._cur_pos > 1)
                self._url = self._next_url
                self.address_bar.setText(self._url.path())

                while self.list_table.rowCount() > 0:
                    self.list_table.removeRow(0)
                self.ftp.list()

    def resizeEvent(self, event):
        maxSize = self.list_table.size().width()
        # Nom Ficher : 40%
        self.list_table.horizontalHeader().resizeSection(0, maxSize*.40)
        # Taille : 30%
        self.list_table.horizontalHeader().resizeSection(1, maxSize*.30)
        event.accept()
