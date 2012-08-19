# coding=utf-8

from ftp import Ftp

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


