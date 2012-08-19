from xml.etree.ElementTree import Element, SubElement
from random import randint

from Share import FileShare, DirectoryShare, AnalyseShare
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
            self.analyse_share = AnalyseShare()

        if "share" in self.opened:
            self.analyse_share.open(name, attrs)

    def endElement(self, name):
        if "share" in self.opened:
            self.analyse_share.close(name, self.buf)
            if self.analyse_share.share:
                self.share_results.append(self.analyse_share.share)
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
