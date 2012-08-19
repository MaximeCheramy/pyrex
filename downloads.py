# coding=utf-8

from ftp import Ftp
from Share import AnalyseShare
from DefaultHandler import DefaultHandler

from PyQt4.QtCore import QUrl

class Download(object):
    def __init__(self, file_share, local_path):
        self._file_share = file_share
        self._local_path = local_path

    @property
    def file_share(self):
        return self._file_share

    @property
    def local_path(self):
        return self._local_path

    @property
    def progress(self):
        return '0.0'

    @property
    def state(self):
        return u'Terminé'

    def start_download(self):
        self.ftp = Ftp(QUrl(self._file_share.url), self._local_path, self.update_progress)

    def update_progress(self, readBytes, totalBytes):
        print "%d / %d" % (readBytes, totalBytes)

class AnalyseDownload(object):
    def __init__(self):
        self.analyse_share = None
        self.share = None
        self.download = None
        self.local_path = None

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
            self.download = Download(self.share, self.local_path)
        elif name == "localpath":
            self.local_path = buf
        elif name == "status":
            self.status = buf
        elif name == "date":
            self.date = date.fromtimestamp(int(buf) / 1000),

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

