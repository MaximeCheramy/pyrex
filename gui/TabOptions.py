#!/usr/bin/python
# coding=utf-8

import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QFileDialog
import os

class TabOptions(QWidget):
    instance = None

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        PyQt4.uic.loadUi('ui/options.ui', self)
        # Si le fichier de config existe pas, on effectue la config par défaut et on le créé
        if not os.path.exists("config.ini"):
            self.defaultConfig()
            self.saveConfig()
        # Sinon on loade le fichier de config
        else:
            self.loadConfig()

    def saveConfig(self):
        d_conf = dict()
        # Configuration Générale
        d_conf["pseudo"]            = str(self.pseudo_edit.text())
        d_conf["save_dir"]          = str(self.dir_button.text())
        d_conf["max_dwl"]           = int(self.spin_max_dwl.value())
        d_conf["nb_res_page"]       = int(self.spin_nb_res_page.value())
        d_conf["eff_dwl_init"]      = str(self.combo_eff_dwl_init.currentIndex())
        d_conf["ico_notif"]         = str(self.combo_ico_notif.currentIndex())
        # Configuration Partages
        d_conf["use_FTP"]           = self.checkBox_FTP.isChecked()
        d_conf["FTP_port"]          = int(self.spin_port.value())
        d_conf["nb_connex_sim"]     = int(self.spin_connex_sim.value())
        d_conf["share_myFiles"]     = self.check_share_myFiles.isChecked()
        d_conf["aff_maListe"]       = self.check_aff_maListe.isChecked()
        # Configuration Avancée
        d_conf["ip_daemon"]         = str(self.edit_IP_daemon.text())
        d_conf["logs"]              = str(self.combo_logs.currentIndex())
        d_conf["nb_ip_scan"]        = int(self.spin_nb_ip_scan.value())
        d_conf["tps_scan"]          = int(self.spin_tps_scan.value())
        d_conf["plage_ip"]          = str(self.edit_plage_ip.text())
        d_conf["ip_conf_daemon"]    = str(self.edit_ip_conf_daemon.text())
        d_conf["aff_myShares"]      = str(self.combo_aff_myShares.currentIndex())
        d_conf["expert_mode"]       = self.check_expert_mode.isChecked()
        # On ecrit la config dans un fichier (config.ini)
        self.writeConfig(d_conf)
        
    def writeConfig(self, d_conf):
        config = open("config.ini", "w")
        for key, value in d_conf.items():
            var = "{}={}\n".format(key,value)
            config.write(var)
        config.close()
            
    def chooseDirectory(self):
        self.dir_button.setText(QFileDialog.getExistingDirectory(self))
        
    def defaultConfig(self, dico=None):
        if dico is None:
            dico = {"pseudo"        : "pseudo", 
                    "save_dir"      : os.path.expanduser('~'), 
                    "max_dwl"       : 10, 
                    "nb_res_page"   : 100, 
                    "eff_dwl_init"  : 1, 
                    "ico_notif"     : 0, 
                    "use_FTP"       : True, 
                    "FTP_port"      : 2221, 
                    "nb_connex_sim" : 10, 
                    "share_myFiles" : True, 
                    "aff_maListe"   : False, 
                    "ip_daemon"     : "127.0.0.1", 
                    "logs"          : 1, 
                    "nb_ip_scan"    : 10, 
                    "tps_scan"      : 120, 
                    "plage_ip"      : "10.31.40.0-10.31.47.254", 
                    "ip_conf_daemon": "", 
                    "aff_myShares"  : 0, 
                    "expert_mode"   : False}
        self.pseudo_edit.setText(dico["pseudo"])
        self.dir_button.setText(dico["save_dir"])
        self.spin_max_dwl.setValue(dico["max_dwl"])
        self.spin_nb_res_page.setValue(dico["nb_res_page"])
        self.combo_eff_dwl_init.setCurrentIndex(dico["eff_dwl_init"])
        self.combo_ico_notif.setCurrentIndex(dico["ico_notif"])
        self.checkBox_FTP.setChecked(dico["use_FTP"])
        self.spin_port.setValue(dico["FTP_port"])
        self.spin_connex_sim.setValue(dico["nb_connex_sim"])
        self.check_share_myFiles.setChecked(dico["share_myFiles"])
        self.check_aff_maListe.setChecked(dico["aff_maListe"])
        self.edit_IP_daemon.setText(dico["ip_daemon"])
        self.combo_logs.setCurrentIndex(dico["logs"])
        self.spin_nb_ip_scan.setValue(dico["nb_ip_scan"])
        self.spin_tps_scan.setValue(dico["tps_scan"])
        self.edit_plage_ip.setText(dico["plage_ip"])
        self.edit_ip_conf_daemon.setText(dico["ip_conf_daemon"])
        self.combo_aff_myShares.setCurrentIndex(dico["aff_myShares"])
        self.check_expert_mode.setChecked(dico["expert_mode"])
        
    def loadConfig(self):
        # On charge la config
        config = open("config.ini", "r")
        dico = dict()
        # On la parse et on met les clés et valeurs dans un dico
        for line in config:
            if "=" in line:
                key, value = line.split("=", 1)
                value = value[:-1]
                # Exception : integer
                try:
                    value = int(value)
                except ValueError:
                    pass
                # Exception : boolean
                if value == 'True':
                    value = True
                elif value == 'False':
                    value = False
                dico[key] = value
            else:
                pass
        config.close()
        # On envoie la config dans Rex
        self.defaultConfig(dico)
