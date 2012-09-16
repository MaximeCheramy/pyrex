from Tools import convert_size_str
from datetime import date

class AnalyseShare(object):
    def __init__(self):
        self.share = None

    def open(self, name, attrs):
        if name == 'share':
            self.data = {'name': '', 'client_address': '', 'path': '',
                    'type': 'file', 'size': '0', 'port': '-1',
                    'nickname': '', 'last_modified': '0', 
                    'protocol': 'FTP'}
            self.share_type = ('type' in attrs) and attrs['type'] or 'file'


    def close(self, name, buf):
         if name == "share":
             if self.share_type == 'file':
                 self.share = FileShare(
                         self.data['name'], self.data['client_address'], 
                         int(self.data['port']), self.data['path'], 
                         self.data['protocol'], float(self.data['size']),
                         date.fromtimestamp(int(self.data['last_modified']) / 1000),
                         self.data['nickname'])
             else:
                 self.share = DirectoryShare(
                         self.data['name'], self.data['client_address'], 
                         int(self.data['port']), self.data['path'], 
                         self.data['protocol'],
                         date.fromtimestamp(int(self.data['last_modified']) / 1000),
                         self.data['nickname'])
         else:
             self.data[name] = buf


class Share(object):
    def __init__(self, name, client_address, port, path, protocol, size, last_modified, nickname, is_directory):
        self._name = name
        self._client_address = client_address
        self._port = port
        self._path = path
        self._protocol = protocol
        self._size = size
        self._last_modified = last_modified
        self._nickname = nickname
        self._is_directory = is_directory

    @property
    def url(self):
        return self._protocol + "://" + self._client_address + ':' + str(self._port) + self._path + self._name

    @property
    def score(self):
        return 1.0

    @property
    def name(self):
        return self._name

    @property
    def client_address(self):
        return self._client_address

    @property
    def port(self):
        return self._port

    @property
    def path(self):
        return self._path

    @property
    def protocol(self):
        return self._protocol

    @property
    def size(self):
        return self._size

    @property
    def str_size(self):
        if self._is_directory:
            return "dossier"
        else:
            return convert_size_str(self._size)

    @property
    def last_modified(self):
        return self._last_modified

    @property
    def str_last_modified(self):
        return self._last_modified.strftime("%d/%m/%y")

    @property
    def nickname(self):
        return self._nickname

class FileShare(Share):
    def __init__(self, name, client_address, port, path, protocol, size, last_modified, nickname):
        Share.__init__(self, name, client_address, port, path, protocol, size, last_modified, nickname, False)

class DirectoryShare(Share):
    def __init__(self, name, client_address, port, path, protocol, last_modified, nickname):
        Share.__init__(self, name, client_address, port, path, protocol, 0, last_modified, nickname, True)
