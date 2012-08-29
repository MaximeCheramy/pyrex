#!/usr/bin/python
# coding=utf-8

import codecs
from confDaemon import ConfDaemon

class Configuration:
    save_dir                    = ""
    max_simultaneous_downloads  = 0
    max_results                 = 0
    clean_dl_list               = 0
    icon                        = 0
    share_downloads             = False
    display_mine                = False
    ip_daemon                   = ""
    log_in_file                 = 0
    adv_mode                    = False
    
    @staticmethod
    def write_config():
        # On écrit dans config.ini tout ce qui se rapporte au gui
        config = codecs.open("config.ini", "w", encoding='utf-8')
        for key, value in Configuration.__dict__.items():
            # On cherche les champs liés au gui
            try:
                var = "{}={}\n".format(key,value)
                # Debug
                #print "{}={}\n".format(key,value)
            except UnicodeEncodeError:
                var = u"{}={}\n".format(key, value)
                # Debug
                #print u"{}={}\n".format(key,value)
            config.write(var)
        config.close()           
        
    @staticmethod
    def load_config():
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
                Configuration.__dict__[key] = value
            else:
                pass
        config.close()       
