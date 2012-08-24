from xml.etree.ElementTree import Element, SubElement
from random import randint

from Share import AnalyseShare
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
    def __init__(self, query, protocol=None, Type=None, extensions="", sizeinf=None, sizesup=None, dateinf=None, datesup=None):
        self.query       = query
        self.protocol    = protocol
        self.Type        = Type
        self.extensions  = extensions
        self.sizeinf     = sizeinf
        self.sizesup     = sizesup
        self.dateinf     = dateinf
        self.datesup     = datesup
        
    def do_search(self, callback):
        search_element = Element('search', 
                           {'ttl': '3', 'id': str(randint(1, 10000000))})
        query_element = SubElement(search_element, 'query')
        query_element.text = self.query
        if self.protocol: 
            protocol_element = SubElement(search_element, 'protocol')
            protocol_element.text = self.protocol
        elif self.Type:
            Type_element = SubElement(search_element, 'type')
            Type_element.text = self.Type
        elif self.extensions:
            extensions_element = SubElement(search_element, 'extensions')
            extensions_element.text = self.extensions
        elif self.sizeinf:
            sizeinf_element = SubElement(search_element, 'sizeinf')
            sizeinf_element.text = str(self.sizeinf)
        elif self.sizesup:
            sizesup_element = SubElement(search_element, 'sizesup')
            sizesup_element.text = str(self.sizesup)
        elif self.dateinf:
            dateinf_element = SubElement(search_element, 'dateinf')
            dateinf_element.text = self.dateinf
        elif self.datesup:
            datesup_element = SubElement(search_element, 'datesup')
            datesup_element.text = self.datesup            
        self.client = Client(search_element, AnalyseResults(callback))
        self.client.start()
