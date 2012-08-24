import PyQt4.uic
from PyQt4.QtGui import QWidget, QTableWidgetItem
from PyQt4.QtCore import pyqtSignal

from peers import PeersGet

class TabPeers(QWidget):
    peersReceived = pyqtSignal(list)
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        PyQt4.uic.loadUi('ui/peers.ui', self)
        self.peers_get = None
        self.peersReceived.connect(self._send_signal_peers)

    def _send_signal_peers(self, peers):
        self.peersReceived.emit(peers)

    def update_peers(self):
        if self.peers_get is None:
            self.peers_get = PeersGet()
            self.peers_get.do_get(self.set_peers)

    def add_peer(self, peer):
        rows = self.table_peers.rowCount()
        self.table_peers.insertRow(rows)
        self.table_peers.setItem(rows, 0, QTableWidgetItem(peer.nickname))
        self.table_peers.setItem(rows, 1, QTableWidgetItem(peer.ip))

    def set_peers(self, peers):
        while self.table_peers.rowCount():
            self.table_peers.removeRow(0)
        for peer in peers:
            self.add_peer(peer)
        self.peers_get = None

