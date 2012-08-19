from xml.etree.ElementTree import Element
from Tools import convert_size_str

from DefaultHandler import DefaultHandler
from Client import Client

class Peer(object):
    def __init__(self, nickname, ip, name, version):
        self._nickname = nickname
        self._ip = ip
        self._name = name
        self._version = version

    @property
    def nickname(self):
        return self._nickname

    @property
    def ip(self):
        return self._ip

    @property
    def name(self):
        return self._name

    @property
    def version(self):
        return self._version


class PeersGet(object):
    def do_get(self, callback):
        search_element = Element('peers', {'type': 'get'})

        self.client = Client(search_element, AnalysePeers(callback))
        self.client.start()

class AnalysePeers(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.callback = callback

    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == 'peers':
            self.peers = []
        elif name == 'peer':
            self.data = {'nickname': '', 'ip': '', 'name': '', 'version': ''}

    def endElement(self, name):
        if name == 'peers':
            self.callback(self.peers)
        elif name == 'peer':
            self.peers.append(Peer(self.data['nickname'], self.data['ip'], self.data['name'], self.data['version']))
        else:
            self.data[name] = self.buf
 
    
