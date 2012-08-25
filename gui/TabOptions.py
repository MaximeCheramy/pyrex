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
            pass

    def saveConfig(self):
        d_conf = dict()
        # Configuration Générale
        d_conf["pseudo"]            = str(self.pseudo_edit.text())
        d_conf["save_dir"]          = str(self.dir_button.text())
        d_conf["max_dwl"]           = int(self.spin_max_dwl.value())
        d_conf["nb_res_page"]       = int(self.spin_nb_res_page.value())
        d_conf["eff_dwl_init"]      = str(self.combo_eff_dwl_init.currentText())
        d_conf["ico_notif"]         = str(self.combo_ico_notif.currentText())
        # Configuration Partages
        d_conf["use_FTP"]           = self.checkBox_FTP.isChecked()
        d_conf["FTP_port"]          = int(self.spin_port.value())
        d_conf["nb_connex_sim"]     = int(self.spin_connex_sim.value())
        d_conf["share_myFiles"]     = self.check_share_myFiles.isChecked()
        d_conf["aff_maListe"]       = self.check_aff_maListe.isChecked()
        # Configuration Avancée
        d_conf["ip_daemon"]         = str(self.edit_IP_daemon.text())
        d_conf["logs"]              = str(self.combo_logs.currentText())
        d_conf["nb_ip_scan"]        = int(self.spin_nb_ip_scan.value())
        d_conf["tps_scan"]          = str(self.edit_tps_scan.text())
        d_conf["plage_ip"]          = str(self.edit_plage_ip.text())
        d_conf["ip_conf_daemon"]    = str(self.edit_ip_conf_daemon.text())
        d_conf["aff_myShares"]      = str(self.combo_aff_myShares.currentText())
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
        
    def defaultConfig(self):
        self.pseudo_edit.setText("pseudo")
        self.dir_button.setText(os.path.expanduser('~'))
        self.spin_max_dwl.setValue(10)
        self.spin_nb_res_page.setValue(100)
        self.combo_eff_dwl_init.setCurrentIndex(1)
        self.combo_ico_notif.setCurrentIndex(0)
        self.checkBox_FTP.setChecked(True)
        self.spin_port.setValue(2221)
        self.spin_connex_sim.setValue(10)
        self.check_share_myFiles.setChecked(True)
        self.check_aff_maListe.setChecked(False)
        self.edit_IP_daemon.setText("127.0.0.1")
        self.combo_logs.setCurrentIndex(1)
        self.spin_nb_ip_scan.setValue(10)
        self.edit_tps_scan.setText("120")
        self.edit_plage_ip.setText("10.31.40.0-10.31.47.254")
        self.edit_ip_conf_daemon.setText("")
        self.combo_aff_myShares.setCurrentIndex(0)
        self.check_expert_mode.setChecked(False)
