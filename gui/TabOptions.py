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
    varsGuiUpdated      = pyqtSignal()
    varsDaemonUpdated   = pyqtSignal()
    varsDaemonToCheck   = pyqtSignal()

    def __init__(self, search, parent=None):
        QWidget.__init__(self, parent)
        PyQt4.uic.loadUi('ui/options.ui', self)
        # Variables de classe
        self.setDefault()
        # Signaux
        self.varsGuiUpdated.connect(self.setGuiVars)
        self.varsDaemonUpdated.connect(self.setDaemonVars)
        self.varsDaemonToCheck.connect(self.checkDaemonVars)
        # Si le fichier de config existe pas, on effectue la config par défaut et on le créé
        if not os.path.exists("config.ini"):
            self.setConfig(True)
            self.saveConfig()
        # Sinon on loade le fichier de config puis on demande la conf au daemon
        else:
            # Debug
            print "On loade la config du GUI"
            conf = Configuration(self.varsGuiUpdated.emit)
            conf.load_config()
            print "On loade la config du Daemon"
            daemon = ConfDaemon(self.varsDaemonUpdated.emit)
            daemon.get_conf()
            
    def saveConfig(self):
        # Configuration Générale
        self.nickname                   = str(self.pseudo_edit.text())
        try:
            self.save_dir               = str(self.dir_button.text())
        except UnicodeEncodeError:
            self.save_dir               = unicode(self.dir_button.text())
        self.max_simultaneous_downloads = int(self.spin_max_dwl.value())
        self.max_results                = int(self.spin_nb_res_page.value())
        self.clean_dl_list              = str(self.combo_eff_dwl_init.currentIndex())
        self.icon                       = str(self.combo_ico_notif.currentIndex())
        # Configuration Partages
        self.ftp_enabled                = self.checkBox_FTP.isChecked()
        self.ftp_port                   = int(self.spin_port.value())
        self.ftp_maxlogins              = int(self.spin_connex_sim.value())
        self.share_downloads            = self.check_share_myFiles.isChecked()
        self.display_mine               = self.check_aff_maListe.isChecked()
        # Configuration Avancée
        self.ip_daemon                  = str(self.edit_IP_daemon.text())
        self.log_in_file                = str(self.combo_logs.currentIndex())
        self.nb_ips_scan_lan            = int(self.spin_nb_ip_scan.value())
        self.time_between_scan          = int(self.spin_tps_scan.value())
        self.ip_range                   = str(self.edit_plage_ip.text())
        self.ips_remote_control         = str(self.edit_ip_conf_daemon.text())
        self.ftp_show_downloads         = str(self.combo_aff_myShares.currentIndex())
        self.adv_mode                   = self.check_expert_mode.isChecked()
        # On ecrit la config du gui dans un fichier (config.ini)
        # Debug
        print "On écrit la nouvelle config du gui"
        configuration = Configuration(None, self.save_dir, self.max_simultaneous_downloads, self.max_results, self.clean_dl_list, self.icon, self.share_downloads, self.display_mine, self.ip_daemon, self.log_in_file, self.adv_mode)
        configuration.write_config()                              
        # On envoie la config du daemon au daemon
        # Debug
        print "On envoie la nouvelle config au daemon"
        daemon = ConfDaemon(self.varsDaemonToCheck.emit, self.nickname, self.time_between_scan, self.nb_ips_scan_lan, self.ip_range, self.ips_remote_control, self.ftp_enabled, self.ftp_port, self.ftp_maxlogins, self.ftp_show_downloads)
        daemon.set_conf()
        
    def setConfig(self, default=None):
        if default:
            # Config par défaut du gui
            self.setDefault()
            # On va chercher la config du daemon
            daemon = ConfDaemon(self.varsDaemonUpdated.emit)
            daemon.get_conf()
        # On affiche la config
        self.pseudo_edit.setText(self.nickname)
        self.dir_button.setText(self.save_dir)
        self.spin_max_dwl.setValue(self.max_simultaneous_downloads)
        self.spin_nb_res_page.setValue(self.max_results)
        self.combo_eff_dwl_init.setCurrentIndex(self.clean_dl_list)
        self.combo_ico_notif.setCurrentIndex(self.icon)
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
    
    def setDefault(self):
        self.nickname                   = "pseudo"
        self.save_dir                   = os.path.expanduser('~')
        self.max_simultaneous_downloads = 10
        self.max_results                = 100
        self.clean_dl_list              = 1
        self.icon                       = 0
        self.ftp_enabled                = True
        self.ftp_port                   = 2221
        self.ftp_maxlogins              = 10
        self.share_downloads            = True
        self.display_mine               = False
        self.ip_daemon                  = "120.0.0.1"
        self.log_in_file                = 1
        self.nb_ips_scan_lan            = 10
        self.time_between_scan          = 120
        self.ip_range                   = "10.31.40.0-10.31.47.254"
        self.ips_remote_control         = ""
        self.ftp_show_downloads         = 0
        self.adv_mode                   = False
        
    def setGuiVars(self, save_dir, max_simultaneous_downloads, max_results, clean_dl_list, icon, share_downloads, display_mine, ip_daemon, log_in_file, adv_mode):
        # Debug
        print "Config reçue du GUI : "
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print 'function name "%s"' % inspect.getframeinfo(frame)[2]
        for i in args:
            print "    %s = %s" % (i, values[i])
        self.save_dir                   = save_dir
        self.max_simultaneous_downloads = max_simultaneous_downloads
        self.max_results                = max_results
        self.clean_dl_list              = clean_dl_list
        self.icon                       = icon
        self.share_downloads            = share_downloads
        self.display_mine               = display_mine
        self.ip_daemon                  = ip_daemon
        self.log_in_file                = log_in_file
        self.adv_mode                   = adv_mode
        
    def setDaemonVars(self, nickname, time_between_scan, nb_ips_scan_lan, ip_range, ips_remote_control, ftp_enabled, ftp_port, ftp_maxlogins, ftp_showdownloads):
        # Debug
        print "Config reçue du daemon : "
        frame = inspect.currentframe()
        args, _, _, values = inspect.getargvalues(frame)
        print 'function name "%s"' % inspect.getframeinfo(frame)[2]
        for i in args:
            print "    %s = %s" % (i, values[i])
        self.nickname           = nickname
        self.time_between_scan  = time_between_scan
        self.nb_ips_scan_lan    = nb_ips_scan_lan
        self.ip_range           = ip_range
        self.ips_remote_control = ips_remote_control
        self.ftp_enabled        = ftp_enabled
        self.ftp_port           = ftp_port
        self.ftp_maxlogins      = ftp_maxlogins
        self.ftp_showdownloads  = ftp_showdownloads
        
    # TODO : vérifier que le daemon a bien pris les modifs et envoyer des erreurs avec cette fonction
    def checkDaemonVars(self, nickname, time_between_scan, nb_ips_scan_lan, ip_range, ips_remote_control, ftp_enabled, ftp_port, ftp_maxlogins, ftp_showdownloads):
        pass
    
    def chooseDirectory(self):
        self.dir_button.setText(QFileDialog.getExistingDirectory(self))
