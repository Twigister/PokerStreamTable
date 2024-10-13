from PyQt6.QtWidgets import QHBoxLayout, QWidget

from qt.PlayerWidget import PlayerWidget

class PlayersWidget(QWidget):
    def __init__(self, P1: PlayerWidget, P2: PlayerWidget):
        super().__init__()
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.resize(400, 600)
        self.P1 = P1
        self.P2 = P2
        layout.addWidget(P1)
        layout.addWidget(P2)
