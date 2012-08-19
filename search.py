from xml.etree.ElementTree import Element, SubElement
from random import randint
from datetime import date

from Share import FileShare, DirectoryShare
from Client import Client
from DefaultHandler import DefaultHandler

class AnalyseResults(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.share_results = None
        self.callback = callback

    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == "results":
            self.share_results  = []

        elif name == "share":
            self.data = {'name': '', 'client_address': '', 'path': '',
                    'type': 'file', 'size': '0', 'port': '-1',
                    'nickname': '', 'last_modified': '0', 
                    'protocol': 'FTP'}

        buffer = ''
    def endElement(self, name):
        if "share" in self.opened:
            if name == "share":
                if self.data["type"] == 'file':
                    self.share_results.append(FileShare(
                            self.data['name'], self.data['client_address'], 
                            int(self.data['port']), self.data['path'], 
                            self.data['protocol'], float(self.data['size']),
                            date.fromtimestamp(int(self.data['last_modified']) / 1000),
                            self.data['nickname']))
                else:
                    self.share_results.append(DirectoryShare(
                            self.data['name'], self.data['client_address'], 
                            int(self.data['port']), self.data['path'], 
                            self.data['protocol'], float(self.data['size']),
                            date.fromtimestamp(int(self.data['last_modified']) / 1000),
                            self.data['nickname']))
            else:
                self.data[name] = self.buf

        else:
            if name == "results":
                self.callback(self.share_results)
        DefaultHandler.endElement(self, name)

class Search(object):
    def __init__(self, query):
        self.query = query
        
    def do_search(self, callback):
        search_element = Element('search', 
                        {'ttl': '3', 'id': str(randint(1, 10000000))})
        query_element = SubElement(search_element, 'query')
        query_element.text = self.query
    
        self.client = Client(search_element, AnalyseResults(callback))
        self.client.start()
