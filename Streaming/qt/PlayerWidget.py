from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QLineEdit

import Table
from utils import fast_type

class PlayerWidget(QWidget):
    def __init__(self, number: int, table: Table):
        super().__init__()
        self.number = number
        self.table = table
        buttonName = QPushButton("Set player name", self)
        buttonName.clicked.connect(self.changeName)
        buttonStack = QPushButton("Set player stack", self)
        buttonStack.clicked.connect(self.setStack)
        buttonAddon = QPushButton("Addon Player", self)
        buttonAddon.clicked.connect(self.addon)
        buttonCards = QPushButton("Set player cards", self)
        buttonCards.clicked.connect(self.setCards)
        self.inputLine = QLineEdit(parent=self)
        self.name = QLabel(table.players[number].name)
        self.stack = QLabel(f"Stack: {self.table.players[number].stack}")
        self.profit = QLabel((f"Profit: {0}"))
        self.eq = QLabel("Current EQ: 50%")
        self.cards = QLabel("Cards: " + str(["?", "?"]))
        self.currentBet = QLabel("Current bet: 0")
        self.label = QLabel(f"P{self.number + 1} dashboard")

        layout = QGridLayout()
        self.setLayout(layout)
        layout.addWidget(self.label, 0, 0, 1, 4)
        layout.addWidget(self.inputLine, 1, 0, 1, 4)
        layout.addWidget(buttonName, 2, 0, 1, 2)
        layout.addWidget(self.name, 2, 2, 1, 1)
        layout.addWidget(buttonStack, 3, 0, 1, 1)
        layout.addWidget(buttonAddon, 3, 1, 1, 1)
        layout.addWidget(self.stack, 3, 2, 1, 1)
        layout.addWidget(self.profit, 3, 3, 1, 1)
        layout.addWidget(buttonCards, 4, 0)
        layout.addWidget(self.cards, 4, 1)
        layout.addWidget(self.currentBet, 4, 2)
        layout.addWidget(self.eq, 4, 3)
    def changeName(self):
        self.table.players[self.number].setName(self.inputLine.text())
        self.label.setText(f"Changed P{self.number + 1} name to: {self.table.players[self.number].name}")
        self.name.setText(self.table.players[self.number].name)
    def setStack(self):
        try:
            value = int(self.inputLine.text())
            self.table.players[self.number].setStack(value)
            self.label.setText(f"Changed P1 stack to {self.table.players[self.number].stack}")
            self.stack.setText(f"Stack: {self.table.players[self.number].stack}")
        except Exception as e:
            print(e)
            self.label.setText("Error: Must be an integer value")
    def addon(self):
        try:
            value = int(self.inputLine.text())
            if (value <= 0):
                raise Exception()                
            self.table.players[self.number].addon(value)
            self.label.setText(f"Addon {value} to {self.table.players[self.number].stack}")
            self.stack.setText(str(self.table.players[self.number].stack))
        except Exception as e:
            print(e)
            self.label.setText("Error: Must be an integer value")
    def setCards(self):
        cards = self.inputLine.text().split(" ")
        if (len(cards) != 2):
            self.label.setText("Error: number of cards invalid")
        else:
            for i in range(2):
                cards[i] = fast_type(cards[i])
            try:
                self.table.players[self.number].setCards(cards)
                self.label.setText("P1 cards update Success")
                self.cards.setText(str(cards))
            except Exception as e:
                print(e)
                self.label.setText("Error: Invalid card")
    def setEq(self):
        self.eq.setText("{0:.0f}%".format(self.table.eq[self.number] * 100))
    def setCurrentBet(self):
        self.currentBet.setText(f"Current bet: {self.table.players[self.number].currentBet}")
    def setCurrentStack(self):
        self.stack.setText(f"Stack: {self.table.players[self.number].stack}")
    def calcProfit(self):
        self.profit.setText(f"Profit: {self.table.players[self.number].stack - self.table.players[self.number].deposit}")
    def refresh(self):
        self.setEq()
        self.setCurrentBet()
        self.setCurrentStack()
        self.calcProfit()
    def resetCards(self):
        self.eq.setText("Eq: 50%")
        self.table.players[self.number].setCards()
        self.cards.setText('["??", "??"]')
