import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import QApplication
from PyQt4.QtNetwork import QFtp

class Ftp(QObject):
    def __init__(self, url, filename, update):
        QObject.__init__(self)

        self.ftp = QFtp(self)
        self.ftp.dataTransferProgress.connect(update)
        
        self.ftp.connectToHost(url.host(), url.port(21))
        self.ftp.login()
        
        self.out_file = QFile(filename)
        if self.out_file.open(QIODevice.WriteOnly):
            self.ftp.get(url.path(), self.out_file)

#app = QApplication(sys.argv)
#ftp = Ftp(QUrl("ftp://localhost:2221/series/chuck.403.avi"), 'out', updateDataTransferProgress)
#sys.exit(app.exec_())
