# coding=utf-8

import time
from datetime import date
from PyQt4.QtCore import QFile, QUrl, QObject, QIODevice, pyqtSignal, QTimer
from PyQt4.QtNetwork import QFtp

from Share import AnalyseShare
from DefaultHandler import DefaultHandler
import Tools

class Downloads(list):
    def __init__(self):
        list.__init__(self)

class Download(QObject):
    def __init__(self, file_share, local_path, date):
        QObject.__init__(self)
        # Variables
        self._file_share = file_share
        self._local_path = local_path
        self._date = date
        self._state = 5
        self._speed = 0
        self._count = 0
        self._last_time = time.time()
        self._last_size = 0

    @classmethod
    def get_download(cls, file_share, local_path, date):
        # TODO DownloadSmb
        return DownloadFtp(file_share, local_path, date)

    @property
    def speed(self):
        return self._speed

    @property
    def date(self):
        return self._date

    @property
    def file_share(self):
        return self._file_share

    @property
    def local_path(self):
        return self._local_path
        
    @property
    def progress(self):
        return 100.0 * float(self.read_bytes) / self._file_share.size

    def get_progress(self):
        p = 100.0 * float(self.read_bytes) / self._file_share.size
        read_bytes_str = Tools.convert_size_str(self.read_bytes)
        return '%d%% (%s / %s)' % (int(p), read_bytes_str, self._file_share.str_size)

    @property
    def state(self):
        if self._state == 1:
            return 'Connexion...'
        elif self._state == 2:
            return u'En attente'
        elif self._state == 3:
            return u'Téléchargement'
        elif self._state == 4:
            return u'Terminé'
        elif self._state == 5:
            return u'En pause'
        elif self._state == 6:
            return u'Connexion interrompue'

class DownloadFtp(Download):
    progressModified    = pyqtSignal(object)
    stateChanged        = pyqtSignal(object)
    downloadFinished    = pyqtSignal(object)
    speedModified       = pyqtSignal(object)
    
    def __init__(self, file_share, local_path, date):
        Download.__init__(self, file_share, local_path, date)
        self.ftp = QFtp(self)
        # Signaux
        self.ftp.dataTransferProgress.connect(self.update_progress)
        self.ftp.done.connect(self.download_finished)
        self.ftp.stateChanged.connect(self.state_changed)
        # Ouverture de fichiers
        self.url = QUrl(self._file_share.url)
        self.out_file = QFile(self.local_path)
        # Vars
        self.read_bytes = self.out_file.size()
        # Timer
        self.timer = QTimer()
        self.timer.start(500)
        self.timer.timeout.connect(self.update_speed)
 
    def start_download(self):
        self.ftp.connectToHost(self.url.host(), self.url.port(21))
        self.ftp.login()
        if self.out_file.open(QIODevice.WriteOnly):
            self.ftp.get(self.url.path(), self.out_file)

    def stop(self):
        self.ftp.close()

    def state_changed(self, state):
        if state == 1 or state == 2:
            self._state = 1
        elif state == 3 or state == 4:
            self._state = 3
        self.stateChanged.emit(self)

    def download_finished(self, _):
        print "finished !"
        self._speed = 0
        self.timer.stop()
        self.downloadFinished.emit(self)
        self.ftp.close()

    def update_speed(self):
        delta = time.time() - self._last_time
        self._speed = float(self.read_bytes - self._last_size) / delta
        self.last_time = time.time()
        self.last_size = self.read_bytes
        self.speedModified.emit(self)
        
    def update_progress(self, read_bytes, total_bytes):
        self.read_bytes = read_bytes
        self.progressModified.emit(self)
        

class AnalyseDownload(object):
    def __init__(self):
        self.analyse_share = None
        self.share = None
        self.download = None
        self.local_path = None
        self.date = None

    def open(self, name, attrs):
        if name == "share":
            self.analyse_share = AnalyseShare()

        if self.analyse_share:
            self.analyse_share.open(name, attrs)

    def close(self, name, buf):
        if self.analyse_share:
            self.analyse_share.close(name, buf)
            if name == "share":
                self.share = self.analyse_share.share
                self.analyse_share = None
        elif name == "download":
            self.download = Download.get_download(self.share, self.local_path, self.date)
        elif name == "localpath":
            self.local_path = buf
        elif name == "status":
            self.status = buf
        elif name == "date":
            self.date = date.fromtimestamp(int(buf) / 1000)

class AnalyseDownloads(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.downloads = None
        self.callback = callback
        self.analyse_download = None

    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == "downloads":
            self.downloads  = []
        elif name == "download":
            self.analyse_download = AnalyseDownload()

        if self.analyse_download:
            self.analyse_download.open(name, attrs)


    def endElement(self, name):
        if "download" in self.opened:
            self.analyse_download.close(name, self.buf)
            if self.analyse_download.download:
                self.downloads.append(self.analyse_download.download)
                self.analyse_download = None
        else:
            if name == "downloads":
                self.callback(self.downloads)
        DefaultHandler.endElement(self, name)

