#!/usr/bin/python
# coding=utf-8

import codecs
import os

class Configuration(object):
    save_dir                    = os.path.expanduser('~')
    max_simultaneous_downloads  = 10
    max_results                 = 100
    clean_dl_list               = 1
    icon                        = 0
    share_downloads             = True
    display_mine                = False
    ip_daemon                   = "127.0.0.1"
    log_in_file                 = 1
    adv_mode                    = False
    close_window                = False
    
    @staticmethod
    def write_config():
        # On écrit dans config.ini tout ce qui se rapporte au gui
        config = codecs.open(os.path.expanduser("~/.pyrex/") + "config.ini", "w", encoding='utf-8')
        for key in ['save_dir', 'max_simultaneous_downloads', 'max_results', 'clean_dl_list', \
                    'icon', 'share_downloads', 'display_mine', 'ip_daemon', 'log_in_file', 'adv_mode', 'close_window']:
            var = u"{}={}\n".format(key, Configuration.__dict__[key])
            config.write(var)
        config.close()           
        
    @staticmethod
    def load_config():
        try:
            # On charge la config
            with codecs.open(os.path.expanduser("~/.pyrex/") + "config.ini", "r", encoding='utf-8') as config:
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
                        setattr(Configuration, key, value)
        except IOError:
            print "Fichier config.ini introuvable, chargement des valeurs par défaut"                        
