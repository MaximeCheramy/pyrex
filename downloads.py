# coding=utf-8

import os
import time
import codecs
from datetime import date

from PyQt4.QtCore import QFile, QUrl, QObject, QIODevice, pyqtSignal, QTimer
from PyQt4.QtNetwork import QFtp

from Share import AnalyseShare
from DefaultHandler import DefaultHandler
from xml.etree.ElementTree import Element, SubElement
import Tools

def status_to_int(status):
    if status == 'waiting':
        return 2
    elif status == 'downloading':
        return 3
    elif status == 'finished':
        return 4
    elif status == 'paused':
        return 5
    elif status == 'error':
        return 7
    else:
        return 1

def int_to_status(status):
    if status == 3:
        return 'downloading'
    elif status == 4:
        return 'finished'
    elif status == '5':
        return 'paused'
    elif status == '7':
        return 'error'
    else:
        return 'waiting'

class Downloads(list):
    def __init__(self):
        list.__init__(self)

    def save(self):
        downloads_element = Element('downloads')
        for download in self:
            download_element = SubElement(downloads_element, 'download')
            SubElement(download_element, 'localpath').text = download.local_path
            SubElement(download_element, 'status').text = int_to_status(download.state)
            try:
                SubElement(download_element, 'date').text = str(int(time.mktime(time.strptime(str(download.date), '%Y-%m-%d')) * 1000))
            except ValueError:
                SubElement(download_element, 'date').text = str(0)
            share_element = download.file_share.xml_element()
            download_element.append(share_element)

        xml_str = Tools.prettify(downloads_element)
        f = codecs.open(os.path.expanduser('~/.pyrex/downloads.xml'), 'w', encoding='utf-8')
        f.write(xml_str)
        f.close()

class Download(QObject):
    def __init__(self, file_share, local_path, date, state):
        QObject.__init__(self)
        # Variables
        self._file_share = file_share
        self._local_path = local_path
        self._date = date
        self._state = state
        self._speed = 0
        self._count = 0
        self._last_time = time.time()
        self._last_size = 0

    @classmethod
    def get_download(cls, file_share, local_path, date, state=1):
        # TODO DownloadSmb
        return DownloadFtp(file_share, local_path, date, state)

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
        return self._state

    @property
    def state_str(self):
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
        elif self._state == 7:
            return u'Error :('

class DownloadFtp(Download):
    progressModified    = pyqtSignal(object)
    stateChanged        = pyqtSignal(object)
    downloadFinished    = pyqtSignal(object)
    speedModified       = pyqtSignal(object)
    
    def __init__(self, file_share, local_path, date, state):
        Download.__init__(self, file_share, local_path, date, state)
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
        self._state = 5
        self.ftp.abort()
        self.timer.stop()
        self.ftp.close()

    def state_changed(self, state):
        if state == 1 or state == 2:
            self._state = 1
        elif state == 3 or state == 4:
            self._state = 3
        self.stateChanged.emit(self)

    def download_finished(self, _):
        print "finished !"
        if self.read_bytes != self.file_share.size:
            self._state = 7
        self._speed = 0
        self.timer.stop()
        self.ftp.abort()
        self.ftp.close()
        self._state = 4
        self.stateChanged.emit(self)
        self.ftp.done.disconnect(self.download_finished)
        self.ftp.stateChanged.disconnect(self.state_changed)
        self.ftp.dataTransferProgress.disconnect(self.update_progress)
        self.downloadFinished.emit(self)

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
            self.download = Download.get_download(self.share, self.local_path, self.date, status_to_int(self.status))
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

