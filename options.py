#!/usr/bin/python
# coding=utf-8

from xml.etree.ElementTree import Element, SubElement
from Client import Client
from DefaultHandler import DefaultHandler

class Options(object):
    def __init__(self, dico):
        self.dico = dico
        
    def set_options(self):
        conf_element = Element('conf', {'type':'set'})
        # Nickname
        pseudo_element = SubElement(conf_element, 'nickname')
        pseudo_element.text = self.dico["pseudo"]
        # Time between scan
        tps_scan_element = SubElement(conf_element, 'time_between_scan')
        tps_scan_element.text = self.dico["tps_scan"]
        # Nb IP à scanner
        ip_scan_element = SubElement(conf_element, 'nb_ips_scan_lan')
        ip_scan_element.text = self.dico["nb_ip_scan"]
        # Plage IP
        plage_ip_element = SubElement(conf_element, 'ip_range')
        plage_ip_element.text = self.dico["plage_ip"]
        # IP config daemon
        ip_conf_daemon_element = SubElement(conf_element, 'ips_remote_control')
        ip_conf_daemon_element.text = self.dico["ip_conf_daemon"]
        # FTP activé
        ftp_enabled_element = SubElement(conf_element, 'ftp_enabled')
        ftp_enabled_element.text = self.dico["use_FTP"]
        # Port FTP
        port_ftp_element = SubElement(conf_element, 'ftp_port')
        port_ftp_element.text = self.dico["FTP_port"]
        # Max Connex simultanées FTP
        max_ftp_login_element = SubElement(conf_element, 'ftp_maxlogins')
        max_ftp_login_element.text = self.dico["nb_connex_sim"]
        # Afficher dwl FTP
        show_ftp_dwl_element = SubElement(conf_element, 'ftp_show_downloads')
        show_ftp_dwl_element.text = self.dico["aff_myShares"]
        # On envoie au client
        #self.client = Client(search_element, AnalyseResults(callback))
        #self.client.start()
        
    def get_options(self):
        conf_element = Element('conf', {'type':'get'})
        #self.client = Client(conf_element, AnalyseOptions(self.dico))
        
class AnalyseOptions(DefaultHandler):
    def __init__(self, dico):
        DefaultHandler.__init__(self)
        self.dico = dico
        
    def startElement(self, name, attrs):
        DefaultHandler.startElement(self, name, attrs)
               
    def endElement(self, name):
        DefaultHandler.endElement(self, name)
