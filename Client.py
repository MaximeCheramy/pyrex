from socket import *
import xml.sax
from xml.etree.ElementTree import tostring
from PyQt4.QtCore import QObject, QRunnable, QThreadPool

from configuration import Configuration

PORT = 1111

class Worker(QRunnable):
    def __init__(self, element, content_handler, hostname):
        QRunnable.__init__(self)
        self.element = element
        self.content_handler = content_handler
        self.hostname = hostname
        self.canceled = False

    def cancel(self):
        self.canceled = True

    def run(self):
        try:
            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect((self.hostname, PORT))
    
            msg = tostring(self.element, 'utf-8')
    
            totalsent = 0
            while len(msg) > totalsent:
                sent = sock.send(msg[totalsent:])
                totalsent += sent
                if sent == 0:
                    break
    
            parser = xml.sax.make_parser()
            parser.setContentHandler(self.content_handler)
    
            while not self.canceled:
                chunk = sock.recv(4096)
                if chunk == '':
                    break
                parser.feed(chunk)
    
        #except socket.error:
        #    pass
        finally:
            sock.close()


class Client(QObject):
    def __init__(self, element, content_handler, hostname=Configuration.ip_daemon):
        QObject.__init__(self)
        self.worker = Worker(element, content_handler, hostname)

    def start(self):
        QThreadPool.globalInstance().start(self.worker)

    def cancel(self):
        self.worker.cancel()
