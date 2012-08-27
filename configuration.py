#!/usr/bin/python
# coding=utf-8

import codecs
from confDaemon import ConfDaemon

class Configuration(object):
    def __init__(self, callback, save_dir="", max_simultaneous_downloads=0, max_results=0, clean_dl_list=0, icon=0, share_downloads=False, display_mine=False, ip_daemon="", log_in_file=0, adv_mode=False):
        self.callback                   = callback
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
        
    def write_config(self):
        # On écrit dans config.ini tout ce qui se rapporte au gui
        config = codecs.open("config.ini", "w", encoding='utf-8')
        for key, value in self.__dict__.items():
            # On cherche les champs liés au gui
            try:
                var = "{}={}\n".format(key,value)
                # Debug
                print "{}={}\n".format(key,value)
            except UnicodeEncodeError:
                var = u"{}={}\n".format(key, value)
                # Debug
                print u"{}={}\n".format(key,value)
            config.write(var)
        config.close()           
        
    def load_config(self):
        # On charge la config
        config = codecs.open("config.ini", "r", encoding='utf-8')
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
                self.__setattr__(key, value)
            else:
                pass
        config.close()
        # On envoie la config à TabOptions
        self.callback(self.save_dir, self.max_simultaneous_downloads, self.max_results, self.clean_dl_list, self.icon, self.share_downloads, self.display_mine, self.ip_daemon, self.log_in_file, self.adv_mode)
