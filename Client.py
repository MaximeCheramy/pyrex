from socket import *
import xml.sax
from xml.etree.ElementTree import tostring
from PyQt4.QtCore import QObject, QRunnable, QThreadPool

HOSTNAME = 'localhost'
PORT = 1111

class Worker(QRunnable):
    def __init__(self, element, content_handler):
        QRunnable.__init__(self)
        self.element = element
        self.content_handler = content_handler

    def run(self):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((HOSTNAME, PORT))

        msg = tostring(self.element, 'utf-8')

        totalsent = 0
        while len(msg) > totalsent:
            sent = sock.send(msg[totalsent:])
            totalsent += sent
            if sent == 0:
                break

        parser = xml.sax.make_parser()
        parser.setContentHandler(self.content_handler)

        while True:
            chunk = sock.recv(4096)
            if chunk == '':
                break
            parser.feed(chunk)

        sock.close()

class Client(QObject):
    def __init__(self, element, content_handler):
        QObject.__init__(self)
        self.worker = Worker(element, content_handler)

    def start(self):
        QThreadPool.globalInstance().start(self.worker)
