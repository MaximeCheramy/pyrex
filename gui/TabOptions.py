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
        # Signaux
        self.varsDaemonUpdated.connect(self.setDaemonVars)
        self.varsDaemonToCheck.connect(self.checkDaemonVars)
        
    def update_conf(self):
        self.setGuiVars()
        print "On loade la config du Daemon"
        self.daemon = ConfDaemon(self.varsDaemonUpdated.emit)
        self.daemon.get_conf()
        self.setConfig()
            
    def saveConfig(self):
        # Configuration Générale
        self.nickname                   = str(self.pseudo_edit.text())
        try:
            self.save_dir               = str(self.dir_button.text())
        except UnicodeEncodeError:
            self.save_dir               = unicode(self.dir_button.text())
        self.max_simultaneous_downloads = int(self.spin_max_dwl.value())
        self.max_results                = int(self.spin_nb_res_page.value())
        #self.clean_dl_list              = int(self.combo_eff_dwl_init.currentIndex())
        self.clean_dl_list              = self.check_clean_dl_list.isChecked()
        #self.icon                       = int(self.combo_ico_notif.currentIndex())
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
        #self.combo_eff_dwl_init.setCurrentIndex(self.clean_dl_list)
        self.check_clean_dl_list.setChecked(self.clean_dl_list)
        #self.combo_ico_notif.setCurrentIndex(self.icon)
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
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print 'function name "%s"' % inspect.getframeinfo(frame)[2]
        for i in args:
            print "    %s = %s" % (i, values[i])
        self.nickname           = daemonVars.nickname
        self.time_between_scan  = daemonVars.time_between_scan
        self.nb_ips_scan_lan    = daemonVars.nb_ips_scan_lan
        self.ip_range           = daemonVars.ip_range
        self.ips_remote_control = daemonVars.ips_remote_control
        self.ftp_enabled        = daemonVars.ftp_enabled
        self.ftp_port           = daemonVars.ftp_port
        self.ftp_maxlogins      = daemonVars.ftp_maxlogins
        self.ftp_show_downloads = daemonVars.ftp_show_downloads
        
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
        
    # TODO : vérifier que le daemon a bien pris les modifs et envoyer des erreurs avec cette fonction
    def checkDaemonVars(self, daemonVars):
        pass
    
    def chooseDirectory(self):
        self.dir_button.setText(QFileDialog.getExistingDirectory(self))
