from xml.etree.ElementTree import Element

from DefaultHandler import DefaultHandler
from Client import Client

class VersionGet(object):
    def do_get(self, callback):
        search_element = Element('version', {'type': 'get'})

        self.client = Client(search_element, AnalyseVersion(callback))
        self.client.start()


class Version(object):
    def __init__(self, name, major_version, minor_version, minor_minor_version):
        self._name = name
        self._major_version = major_version
        self._minor_version = minor_version
        self._minor_minor_version = minor_minor_version

    @property
    def name(self):
        return self._name

    @property
    def major(self):
        return self._major_version

    @property
    def minor(self):
        return self._minor_version

    @property
    def minor_minor(self):
        return self._minor_minor_version


class AnalyseVersion(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.callback = callback

    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == 'version':
		self.data = {'name': '', 'major_version': '0', 'minor_version': '0', 'minor_minor_version': '0'}

    def endElement(self, name):
        if name == 'version':
            self.callback(Version(self.data['name'],
                          int(self.data['major_version']),
                          int(self.data['minor_version']), 
                          int(self.data['minor_minor_version'])))
        else:
            self.data[name] = self.buf

        DefaultHandler.endElement(self, name)
