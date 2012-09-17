import PyQt4.uic
from PyQt4.QtGui import QWidget, QTableWidgetItem, QApplication, QMenu
from PyQt4.QtCore import pyqtSignal, QTimer, Qt, SIGNAL

from peers import PeersGet
from stats import StatisticsGet

class TabPeers(QWidget):
    peersReceived = pyqtSignal(list)
    statsReceived = pyqtSignal(object)
    def __init__(self, tabs_results, tabs):
        QWidget.__init__(self, tabs)
        self.tabs_results = tabs_results
        self.tabs         = tabs
        # Load de l'UI
        PyQt4.uic.loadUi('ui/peers.ui', self)
        # Vars
        self.peers_get  = None
        self.stats_get  = None
        self.timer      = None
        self.cache      = {}
        # Config affichage
        self.table_peers.sortItems(0)
        #self.table_peers.setStyleSheet(\
        #        "QTableView::item{ \
        #         border-right-style:solid; \
        #         border-width:0.5; \
        #         border-color: #9B9B9B; \
        #         }")
        # On autorise la creation de menu contextuel
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # Signaux
        self.customContextMenuRequested.connect(self.contextMenu)
        self.peersReceived.connect(self.set_peers)
        self.statsReceived.connect(self.set_stats)

    def update_peers(self):
        if self.peers_get is None:
            self.peers_get = PeersGet()
            self.peers_get.do_get(self.peersReceived.emit)

    def add_peer(self, peer):
        rows = self.table_peers.rowCount()
        self.table_peers.insertRow(rows)
        item = QTableWidgetItem(peer.nickname)
        item.peer = peer
        self.table_peers.setItem(rows, 0, item)
        self.table_peers.setItem(rows, 1, QTableWidgetItem(peer.ip))

    def set_peers(self, peers):
        while self.table_peers.rowCount():
            self.table_peers.removeRow(0)
        self.table_peers.setSortingEnabled(False)
        for peer in peers:
            self.add_peer(peer)
        self.peers_get = None
        self.table_peers.setSortingEnabled(True)

    def set_stats(self, stats):
        if stats:
            self.cache[stats.ip] = stats
            row = self.table_peers.currentRow()
            if row >= 0 and self.table_peers.item(row, 0).peer.ip == stats.ip:
                self.label_size_shares.setText(stats.shares_size_mine_str)
                self.label_size_total_shares.setText(stats.shares_size_total_str)
                self.label_peers.setText(str(stats.users))
        else:
            if self.timer:
                self.timer.stop()
            self.timer = QTimer()
            self.timer.setSingleShot(True)
            self.timer.start(1000)
            self.timer.timeout.connect(self.stats_get.do_get)

    def cell_selected(self, row, col, prev_row, prev_col):
        if row >= 0:
            item = self.table_peers.item(row, 0)
            self.label_nickname.setText(item.peer.nickname)
            self.label_ip.setText(item.peer.ip)
            self.label_version.setText("%s %s" %
                            (item.peer.name, item.peer.version))

            if item.peer.ip in self.cache:
                self.set_stats(self.cache[item.peer.ip])
            else:
                self.label_size_shares.setText('-')
                self.label_size_total_shares.setText('-')
                self.label_peers.setText('-')

            self.stats_get = StatisticsGet(self.statsReceived.emit, item.peer.ip)
            self.stats_get.do_get()
            
    def contextMenu(self, pos):
        menu = QMenu()
        # Actions
        showAction      = menu.addAction("Afficher ses partages")
        copyAction      = menu.addAction("Copier l'IP")
        # Signaux
        self.connect(showAction, SIGNAL('triggered()'), self.show_Action)
        self.connect(copyAction, SIGNAL('triggered()'), self.copy_Action)
        # On affiche le menu
        menu.exec_(self.mapToGlobal(pos))
        
    def getPeer(self):
        row = self.table_peers.currentRow()
        return self.table_peers.item(row, 0).peer
        
    def show_Action(self):
        print "TODO"
                
    def copy_Action(self):
        pressPaper = QApplication.clipboard()
        pressPaper.setText(self.getPeer().ip)
        
    def resizeEvent(self, event):
        maxSize = self.table_peers.size().width()
        # Pseudo : 35%
        self.table_peers.horizontalHeader().resizeSection(0, maxSize*.35)
        event.accept()       
