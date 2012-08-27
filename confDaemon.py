#!/usr/bin/python
# coding=utf-8

from xml.etree.ElementTree import Element, SubElement
from Client import Client
from DefaultHandler import DefaultHandler

class ConfDaemon(object):
    def __init__(self, callback, nickname=None, time_between_scan=None, nb_ips_scan_lan=None, ip_range=None, ips_remote_control=None, ftp_enabled=None, ftp_port=None, ftp_maxlogins=None, ftp_show_downloads=None):
        self.callback           = callback
        self.nickname           = nickname
        self.time_between_scan  = time_between_scan
        self.nb_ips_scan_lan    = nb_ips_scan_lan
        self.ip_range           = ip_range
        self.ips_remote_control = ips_remote_control
        self.ftp_enabled        = ftp_enabled
        self.ftp_port           = ftp_port
        self.ftp_maxlogins      = ftp_maxlogins
        self.ftp_show_downloads  = ftp_show_downloads
        
    def set_conf(self):
        set_conf_element = Element('conf', {'type':'set'})
        # Nickname
        nickname_element = SubElement(set_conf_element, 'nickname')
        nickname_element.text = self.nickname
        # Time between scan
        time_between_scan_element = SubElement(set_conf_element, 'time_between_scan')
        time_between_scan_element.text = self.time_between_scan
        # Nb IP à scanner
        nb_ips_scan_lan_element = SubElement(set_conf_element, 'nb_ips_scan_lan')
        nb_ips_scan_lan_element.text = self.nb_ips_scan_lan
        # Plage IP
        ip_range_element = SubElement(set_conf_element, 'ip_range')
        ip_range_element.text = self.ip_range
        # IP config daemon
        ips_remote_control_element = SubElement(set_conf_element, 'ips_remote_control')
        ips_remote_control_element.text = self.ips_remote_control
        # FTP activé
        ftp_enabled_element = SubElement(set_conf_element, 'ftp_enabled')
        ftp_enabled_element.text = self.ftp_enabled
        # Port FTP
        ftp_port_element = SubElement(set_conf_element, 'ftp_port')
        ftp_port_element.text = self.ftp_port
        # Max Connex simultanées FTP
        ftp_maxlogins_element = SubElement(set_conf_element, 'ftp_maxlogins')
        ftp_maxlogins_element.text = self.ftp_maxlogins
        # Afficher dwl FTP
        ftp_show_downloads_element = SubElement(set_conf_element, 'ftp_show_downloads')
        ftp_show_downloads_element.text = self.ftp_show_downloads
        # On envoie au client
        self.client = Client(set_conf_element, AnalyseConfDaemon(self.callback))
        self.client.start()
        
    def get_conf(self):
        get_conf_element = Element('conf', {'type':'get'})
        self.client = Client(get_conf_element, AnalyseConfDaemon(self.callback))
        self.client.start
        
class AnalyseConfDaemon(DefaultHandler):
    def __init__(self, callback):
        DefaultHandler.__init__(self)
        self.callback = callback
        
    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
        if name == "conf":
            self.data = {'nickname'             : "",
                         'time_between_scan'    : 0,
                         'nb_ips_scan_lan'      : 0,
                         'ip_range'             : "",
                         'ips_remote_control'   : "",
                         'ftp_enabled'          : None,
                         'ftp_port'             : 0,
                         'ftp_maxlogins'        : 0,
                         'ftp_showdownloads'    : None}

    def endElement(self, name):
        if name == "conf":
            self.callback(ConfDaemon(None, self.data["nickname"], self.data["time_between_scan"], self.data["nb_ips_scan_lan"], self.data["ip_range"], self.data["ips_remote_control"], self.data["ftp_enabled"], self.data["ftp_port"], self.data["ftp_maxlogins"], self.data["ftp_showdownloads"]))
        else:
            self.data[name] = self.buf
        DefaultHandler.endElement(self, name)
