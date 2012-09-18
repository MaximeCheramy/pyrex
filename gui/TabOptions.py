#!/usr/bin/python
# coding=utf-8

import os
import PyQt4.uic
from PyQt4.QtCore import *
from PyQt4.QtGui import QWidget, QFileDialog
from confDaemon import ConfDaemon
from configuration import Configuration

# A supprimer (debug)
import inspect

class TabOptions(QWidget):
    instance            = None
    varsDaemonUpdated   = pyqtSignal(object)
    varsDaemonToCheck   = pyqtSignal(object)

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        PyQt4.uic.loadUi('ui/options.ui', self)
        # Variables du daemon : au cas ou il ne répondrait pas
        self.setDaemonVarsDefault()
        # Config initiale affichage
        self.setExpertMode(self.check_expert_mode.isChecked())
        # Signaux
        self.varsDaemonUpdated.connect(self.setDaemonVars)
        self.varsDaemonToCheck.connect(self.checkDaemonVars)
        QObject.connect(self.check_expert_mode, SIGNAL('stateChanged(int)'), self. setExpertMode)
        #########################################################
        # On désactive les boutons qui sont pas encore implantés
        self.spin_max_dwl.setEnabled(False)
        self.spin_nb_res_page.setEnabled(False)
        self.check_clean_dl_list.setEnabled(False)
        self.combo_logs.setEnabled(False)  
        #########################################################  
        
    def update_conf(self):
        self.setGuiVars()
        print "On loade la config du Daemon"
        self.daemon = ConfDaemon(self.varsDaemonUpdated.emit)
        self.daemon.get_conf()
                    
    def saveConfig(self):
        # Configuration Générale
        self.nickname                   = str(self.pseudo_edit.text())
        try:
            self.save_dir               = str(self.dir_button.text())
        except UnicodeEncodeError:
            self.save_dir               = unicode(self.dir_button.text())
        self.max_simultaneous_downloads = int(self.spin_max_dwl.value())
        self.max_results                = int(self.spin_nb_res_page.value())
        self.clean_dl_list              = self.check_clean_dl_list.isChecked()
        self.icon                       = self.check_icon.isChecked()
        # Configuration Partages
        self.ftp_enabled                = self.checkBox_FTP.isChecked()
        self.ftp_port                   = int(self.spin_port.value())
        self.ftp_maxlogins              = int(self.spin_connex_sim.value())
        self.share_downloads            = self.check_share_myFiles.isChecked()
        self.display_mine               = self.check_aff_maListe.isChecked()
        # Configuration Avancée
        self.ip_daemon                  = str(self.edit_IP_daemon.text())
        self.log_in_file                = int(self.combo_logs.currentIndex())
        self.nb_ips_scan_lan            = int(self.spin_nb_ip_scan.value())
        self.time_between_scan          = int(self.spin_tps_scan.value())
        self.ip_range                   = str(self.edit_plage_ip.text())
        self.ips_remote_control         = str(self.edit_ip_conf_daemon.text())
        self.ftp_show_downloads         = int(self.combo_aff_myShares.currentIndex())
        self.adv_mode                   = self.check_expert_mode.isChecked()
        # On ecrit la config du gui dans un fichier (config.ini)
        # Debug
        print "On écrit la nouvelle config du gui"
        Configuration.save_dir                      = self.save_dir
        Configuration.max_simultaneous_downloads    = self.max_simultaneous_downloads
        Configuration.max_results                   = self.max_results
        Configuration.clean_dl_list                 = self.clean_dl_list
        Configuration.icon                          = self.icon
        Configuration.share_downloads               = self.share_downloads
        Configuration.display_mine                  = self.display_mine
        Configuration.ip_daemon                     = self.ip_daemon
        Configuration.log_in_file                   = self.log_in_file
        Configuration.adv_mode                      = self.adv_mode
        Configuration.write_config()                              
        # On envoie la config du daemon au daemon
        # Debug
        print "On envoie la nouvelle config au daemon"
        daemon = ConfDaemon(self.varsDaemonToCheck.emit, self.nickname, self.time_between_scan, self.nb_ips_scan_lan, self.ip_range, self.ips_remote_control, self.ftp_enabled, self.ftp_port, self.ftp_maxlogins, self.ftp_show_downloads)
        daemon.set_conf()
        
    def setConfig(self):
        # On affiche la config
        self.pseudo_edit.setText(self.nickname)
        self.dir_button.setText(self.save_dir)
        self.spin_max_dwl.setValue(self.max_simultaneous_downloads)
        self.spin_nb_res_page.setValue(self.max_results)
        self.check_clean_dl_list.setChecked(self.clean_dl_list)
        self.check_icon.setChecked(self.icon)
        self.checkBox_FTP.setChecked(self.ftp_enabled)
        self.spin_port.setValue(self.ftp_port)
        self.spin_connex_sim.setValue(self.ftp_maxlogins)
        self.check_share_myFiles.setChecked(self.share_downloads)
        self.check_aff_maListe.setChecked(self.display_mine)
        self.edit_IP_daemon.setText(self.ip_daemon)
        self.combo_logs.setCurrentIndex(self.log_in_file)
        self.spin_nb_ip_scan.setValue(self.nb_ips_scan_lan)
        self.spin_tps_scan.setValue(self.time_between_scan)
        self.edit_plage_ip.setText(self.ip_range)
        self.edit_ip_conf_daemon.setText(self.ips_remote_control)
        self.combo_aff_myShares.setCurrentIndex(self.ftp_show_downloads)
        self.check_expert_mode.setChecked(self.adv_mode)
        
    def setGuiVars(self):
        self.save_dir                   = Configuration.save_dir
        self.max_simultaneous_downloads = Configuration.max_simultaneous_downloads
        self.max_results                = Configuration.max_results
        self.clean_dl_list              = Configuration.clean_dl_list
        self.icon                       = Configuration.icon
        self.share_downloads            = Configuration.share_downloads
        self.display_mine               = Configuration.display_mine
        self.ip_daemon                  = Configuration.ip_daemon
        self.log_in_file                = Configuration.log_in_file
        self.adv_mode                   = Configuration.adv_mode
        
    def setDaemonVars(self, daemonVars):
        # Debug
        print "Config reçue du daemon : "
        #print "Nickname :", daemonVars.nickname
        #print "Time_between_scan :", daemonVars.time_between_scan
        #print "Nb_ips_scan_lan :", daemonVars.nb_ips_scan_lan
        #print "Ip_range :", daemonVars.ip_range
        #print "Ips_remote_control :", daemonVars.ips_remote_control
        #print "Ftp_enabled :", daemonVars.ftp_enabled
        #print "Ftp_port :", daemonVars.ftp_port
        #print "Ftp_maxlogins :", daemonVars.ftp_maxlogins
        #print "Ftp_show_downloads :", daemonVars.ftp_show_downloads
        
        self.nickname           = daemonVars.nickname
        self.time_between_scan  = int(daemonVars.time_between_scan)
        self.nb_ips_scan_lan    = int(daemonVars.nb_ips_scan_lan)
        self.ip_range           = daemonVars.ip_range
        self.ips_remote_control = daemonVars.ips_remote_control
        if daemonVars.ftp_enabled == "true":
            self.ftp_enabled    = True
        else:
            self.ftp_enabled    = False
        self.ftp_port           = int(daemonVars.ftp_port)
        self.ftp_maxlogins      = int(daemonVars.ftp_maxlogins)
        if daemonVars.ftp_show_downloads == "true":
            self.ftp_show_downloads = True
        else:
            self.ftp_show_downloads = False
        # On écrit la config
        self.setConfig()
        
    def setDaemonVarsDefault(self):
        self.nickname           = ""
        self.time_between_scan  = 0
        self.nb_ips_scan_lan    = 0
        self.ip_range           = "0"
        self.ips_remote_control = "0"
        self.ftp_enabled        = False
        self.ftp_port           = 0
        self.ftp_maxlogins      = 0
        self.ftp_show_downloads  = 0
        
    def setExpertMode(self, active):
        if active:
            self.spin_nb_ip_scan.show()     ; self.label_32.show()
            self.spin_tps_scan.show()       ; self.label_34.show()
            self.edit_plage_ip.show()       ; self.label_35.show()
            self.edit_ip_conf_daemon.show() ; self.label_33.show()
            self.combo_aff_myShares.show()  ; self.label_36.show()
        else:
            self.spin_nb_ip_scan.hide()     ; self.label_32.hide()
            self.spin_tps_scan.hide()       ; self.label_34.hide()
            self.edit_plage_ip.hide()       ; self.label_35.hide()
            self.edit_ip_conf_daemon.hide() ; self.label_33.hide()
            self.combo_aff_myShares.hide()  ; self.label_36.hide()
        
    # TODO : vérifier que le daemon a bien pris les modifs et envoyer des erreurs avec cette fonction
    def checkDaemonVars(self, daemonVars):
        pass
    
    def chooseDirectory(self):
        self.dir_button.setText(QFileDialog.getExistingDirectory(self, u"Sélectionnez un dossier", os.path.expanduser("~")))
