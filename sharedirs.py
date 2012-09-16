# coding=utf-8

from xml.etree.ElementTree import Element, SubElement

from DefaultHandler import DefaultHandler
from Client import Client

class ShareDir(object):
    def __init__(self, name, path):
        self._name = name
        self._path = path

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path


class SharedirsGet(object):
    def do_get(self, callback):
        search_element = Element('sharedirs', {'type': 'get'})
        self.client = Client(search_element, AnalyseSharedirs(callback))
        self.client.start()

class SharedirsSet(object):
    def do_set(self, sharedirs, callback):
        sharedirs_element = Element('sharedirs')
        #TODO : gérer l'utf-8 (é) ...
        for sharedir in sharedirs:
           sharedir_element = SubElement(sharedirs_element, 'sharedir', {'name':sharedir.name, 'path':sharedir.path})
        self.client = Client(sharedirs_element, AnalyseSharedirs(callback))
        self.client.start()

class AnalyseSharedirs(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.callback = callback
        self.sharedirs = None

    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == 'sharedirs':
            self.sharedirs = []
        elif name == 'sharedir':
            if 'name' in attrs and 'path' in attrs:
                self.sharedirs.append(ShareDir(attrs['name'], attrs['path']))

    def endElement(self, name):
        if name == 'sharedirs':
            self.callback(self.sharedirs)

