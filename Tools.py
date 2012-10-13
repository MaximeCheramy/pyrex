from xml.etree import ElementTree
from xml.dom import minidom
import sys, subprocess, os

GIBI = 1024.0 * 1024 * 1024
MEBI = 1024.0 * 1024
KIBI = 1024.0

def convert_size_str(size):
    if size > GIBI:
        str_size = "%.2f Gio" % (size / GIBI)
    elif size > MEBI:
        str_size = "%.2f Mio" % (size / MEBI)
    elif size > KIBI:
        str_size = "%.2f Kio" % (size / KIBI)
    else:
        str_size = "%.2f o" % (size)
    return str_size

def convert_speed_str(speed):
    if speed > MEBI:
        str_speed = "{0:.1f} {1}".format(speed / MEBI, "Mio/s")
    elif speed > KIBI:
        str_speed = "{0:.1f} {1}".format(speed / KIBI, "Kio/s")
    elif speed > 0:
        str_speed = "{0:.1f} {1}".format(speed, "o/s")
    else:
        str_speed = "0 Kio/s"
    return str_speed

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def open_file(filepath):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', filepath))
    elif os.name == 'nt':
        os.startfile(filepath)
    elif os.name == 'posix':
        subprocess.call(('xdg-open', filepath))

