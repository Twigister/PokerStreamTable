from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from PyQt6 import QtGui
from PyQt6.QtCore import Qt

from qt.PlayersWidget import PlayersWidget
from qt.PlayerWidget import PlayerWidget

import traceback
from CustomErr import CustomErr

from qt.PlayersWidget import PlayersWidget
from qt.PlayerWidget import PlayerWidget
from Table import Table
from utils import *
import globalv
import options

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Poker Stream Deck")
        self.table = Table()
        self.PlayersWidget = PlayersWidget(PlayerWidget(0, self.table), PlayerWidget(1, self.table))
        self.setWindowIcon(QtGui.QIcon('ressources/logo.png'))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputLine = QLineEdit(parent=self)

        buttonBoard = QPushButton("Set board", self)
        buttonBoard.clicked.connect(self.setBoard)
        buttondealer = QPushButton("Change Dealer", self)
        buttondealer.clicked.connect(self.table.changeDealer)
        buttonBlinds = QPushButton("Set blinds", self)
        buttonBlinds.clicked.connect(self.setBlinds)
        buttonNewHand = QPushButton("New Hand", self)
        buttonNewHand.clicked.connect(self.table.newHand)
        buttonEQ = QPushButton("EQ calculator", self)
        buttonEQ.clicked.connect(self.calcEq)
        buttonPostBlinds = QPushButton("Post Blinds", self)
        buttonPostBlinds.clicked.connect(self.postBlinds)
        buttonCall = QPushButton("Check/Call", self)
        buttonCall.clicked.connect(self.call)
        buttonBet = QPushButton("Bet", self)
        buttonBet.clicked.connect(self.bet)
        buttonFold = QPushButton("Fold", self)
        buttonFold.clicked.connect(self.fold)

        changeToMain = QPushButton("Change to main scene")
        changeToMain.clicked.connect(self.swapSceneMain)
        layout.addWidget(changeToMain)

        changeToResults = QPushButton("Change to results")
        changeToResults.clicked.connect(self.swapSceneResults)
        layout.addWidget(changeToResults)

        self.label = QLabel("Coucou toi")
        layout.addWidget(self.PlayersWidget)


        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(buttonBoard)
        layout.addWidget(buttondealer)
        layout.addWidget(buttonBlinds)
        layout.addWidget(buttonNewHand)
        layout.addWidget(buttonEQ)
        layout.addWidget(buttonPostBlinds)
        layout.addWidget(buttonCall)
        layout.addWidget(buttonBet)
        layout.addWidget(buttonFold)
        layout.addWidget(self.inputLine)
    def setBoard(self):
        try:
            if (self.inputLine.text() != ""):
                board = self.inputLine.text().split(" ")
            else:
                board = []
            for i in range(len(board)):
                board[i] = fast_type(board[i])
            if not valid_config(self.table.players[0].cards, self.table.players[1].cards, board):
                raise CustomErr("Invalid config")
            self.table.setBoard(board)
            self.calcEq()
            self.label.setText("Successfully updated board")
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.label.setText("Error: Invalid cards")
    def setBlinds(self):
        try:
            tab = self.inputLine.text()
            tab = tab.split(" ")
            if len(tab) != 2:
                raise CustomErr
            self.table.setBlinds(int(tab[0]), int(tab[1]))
        except Exception as e:
            print(e)
            self.label.setText("Error: Invalid input")
    def resetCards(self):
        self.table.resetCards()
        self.PlayersWidget.P1.resetCards()
        self.PlayersWidget.P2.resetCards()
    def calcEq(self):
        try:
            self.table.calcEq()
            self.label.setText("Equity calculation success")
            self.PlayersWidget.P1.setEq()
            self.PlayersWidget.P2.setEq()
        except Exception as e:
            print(e)
            self.label.setText("Error in eq calculation")
    def postBlinds(self):
        self.table.postBlinds()
        self.PlayersWidget.P1.refresh()
        self.PlayersWidget.P2.refresh()
    def call(self):
        self.table.call()
        self.PlayersWidget.P1.refresh()
        self.PlayersWidget.P2.refresh()
    def bet(self):
        amount = self.inputLine.text()
        try:
            amount = int(amount)
            self.table.bet(amount)
            self.PlayersWidget.P1.refresh()
            self.PlayersWidget.P2.refresh()
        except Exception as e:
            print(e)
            self.label.setText("Error: Should be a positive number")
    def fold(self):
        self.table.fold()
        self.PlayersWidget.P1.refresh()
        self.PlayersWidget.P2.refresh()
    def swapSceneMain(self):
        globalv.cl.send("SetCurrentProgramScene", {"sceneName": options.MainSceneName})
    def swapSceneResults(self):
        P1_profit = self.table.players[0].stack - self.table.players[0].deposit
        globalv.cl.send("SetCurrentProgramScene", {"sceneName": options.ResultsSceneName})
        globalv.cl.send("SetInputSettings", {"inputName": "P1_profit", "inputSettings": {"text": str(P1_profit)}})
        globalv.cl.send("SetInputSettings", {"inputName": "P2_profit", "inputSettings": {"text": str(-P1_profit)}})
        globalv.cl.send("SetSceneItemTransform", {"sceneName": options.ResultsSceneName, "sceneItemId": get_item_id("P1_profit", options.ResultsSceneName, globalv.cl), "sceneItemTransform": {"positionY": 230 + int(P1_profit <= 0) * 355}})
        globalv.cl.send("SetSceneItemTransform", {"sceneName": options.ResultsSceneName, "sceneItemId": get_item_id("P2_profit", options.ResultsSceneName, globalv.cl), "sceneItemTransform": {"positionY": 230 + int(P1_profit > 0) * 355}})
        globalv.cl.send("SetSceneItemTransform", {"sceneName": options.ResultsSceneName, "sceneItemId": get_item_id("P1_name", options.ResultsSceneName, globalv.cl), "sceneItemTransform": {"positionY": 230 + int(P1_profit <= 0) * 355}})
        globalv.cl.send("SetSceneItemTransform", {"sceneName": options.ResultsSceneName, "sceneItemId": get_item_id("P2_name", options.ResultsSceneName, globalv.cl), "sceneItemTransform": {"positionY": 230 + int(P1_profit > 0) * 355}})
    def setCard(self, playerno: int, cardno: int, card: str):
        print("¯\\_(ツ)_/¯")
        tempcards = self.table.players[playerno].cards
        print("Cards retrieved")
        tempcards[cardno] = fast_type(card)
        print(str(tempcards))
        if playerno == 0:
            fun1 = self.PlayersWidget.P1.cards.setText
        elif playerno == 1:
            fun1 = self.PlayersWidget.P2.cards.setText
        self.table.setCard(playerno, cardno, card)
        fun1(str(tempcards))
        self.PlayersWidget.P1.setEq()
        self.PlayersWidget.P2.setEq()
        print("Window.setCard success!")
    def setBoardCard(self, cardno: int, card: str):
        tempboard = self.table.board
        if len(tempboard) <= cardno:
            for _ in range(cardno - len(tempboard) + 1):
                tempboard.append("??")
        tempboard[cardno] = card
        for i in range(len(tempboard)):
            if (tempboard[i] != "??"):
                tempboard[i] = fast_type(tempboard[i])
        print(f"changing {tempboard} [{cardno}] card to {card}")
        print(tempboard[cardno])
        print(f"new board should be: {tempboard}")
        if (valid_config(self.table.players[0].cards, self.table.players[1].cards, tempboard)):
            print("Valid config, setting up board")
            self.table.setBoard(self.table.board)
            print("table.setBoard success")
            self.table.calcEq()
        else:
            print("Invalid config")
