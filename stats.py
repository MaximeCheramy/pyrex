from xml.etree.ElementTree import Element
from Tools import convert_size_str

from DefaultHandler import DefaultHandler
from Client import Client
from configuration import Configuration

class StatisticsGet(object):
    def __init__(self, callback, hostname=Configuration.ip_daemon):
        self.hostname = hostname
        self.callback = callback

    def do_get(self):
        search_element = Element('statistics', {'type': 'get'})
        self.client = Client(search_element, AnalyseStatistics(self.callback), self.hostname)
        self.client.start()

    def cancel(self):
        self.client.cancel()


class Statistics(object):
    def __init__(self, nickname, ip, users, shares_size_total, shares_size_mine):
        self._nickname = nickname
        self._ip = ip
        self._users = users
        self._shares_size_total = shares_size_total
        self._shares_size_mine = shares_size_mine

    @property
    def ip(self):
        return self._ip

    @property
    def nickname(self):
        return self._nickname

    @property
    def users(self):
        return self._users

    @property
    def shares_size_total(self):
        return self._shares_size_total

    @property
    def shares_size_total_str(self):
        return convert_size_str(self._shares_size_total)

    @property
    def shares_size_mine_str(self):
        return convert_size_str(self._shares_size_mine)

    @property
    def shares_size_mine(self):
        return self._shares_size_mine

class AnalyseStatistics(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.callback = callback

    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == 'statistics':
            self.data = {'nickname': '', 'ip': '', 'users': '0', 'shares_size_total': '0', 'shares_size_mine': '0'}
            
    def endElement(self, name):
        if name == 'error':
            self.callback(None)
        elif name == 'statistics':
            self.callback(Statistics(self.data['nickname'], 
                                     self.data['ip'],
                                     int(self.data['users']), 
                                     float(self.data['shares_size_total']),
                                     float(self.data['shares_size_mine'])))
        else:
            self.data[name] = self.buf

        DefaultHandler.endElement(self, name)
