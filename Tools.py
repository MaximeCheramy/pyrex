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
