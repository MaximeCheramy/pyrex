from xml.sax.handler import ContentHandler

class DefaultHandler(ContentHandler):
    def __init__(self):
        self.opened = []
    def startElement(self, name, attrs):
        self.opened.append(name)
        self.buf = ''
    def endElement(self, name):
        self.opened.pop()
    def characters(self, content):
        self.buf += content

