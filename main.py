from PyQt6.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
import keys
from utils import *
import probas
import obsws_python as obs

class Player():
    def __init__(self, name: str, number: int):
        super().__init__()
        self.name = name
        self.number = number
        self.stack = 0
        self.currentBet = 0
        self.deposit = 0
        self.cards = ["??", "??"]
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": "Sat in"}})
    def setName(self, name: str):
        self.name = name
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_name", "inputSettings": {"text": name}})
    def setStack(self, stack: int):
        self.stack = stack
        self.deposit = stack
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(stack)}})
    def setCards(self, cards: [str, str] = ["??", "??"]):
        self.cards = cards
        print(cards)
        for i in range(2):
            card = cards[i]
            print(card)
            if (card == "??"):
                cl.send("SetInputSettings", {"inputName": f"Carte{self.number}-{i + 1}", "inputSettings": {"text": "??", "color": 0}})
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id(f"Carte{self.number}-{i + 1}?", cl), "sceneItemEnabled": True})
            elif is_valid_card(card):
                cl.send("SetInputSettings", {"inputName": f"Carte{self.number}-{i + 1}", "inputSettings": {"text": cards[i], "color": color_code[cards[i][1]]}})
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id(f"Carte{self.number}-{i + 1}?", cl), "sceneItemEnabled": False})
            else:
                self.setCards()
    def addon(self, amount: int):
        self.stack += amount
        self.deposit += amount
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def postBlinds(self, amount: int, isBB: bool):
        if isBB:
            message = f"Posts BB: {amount}"
        else:
            message = f"Posts SB: {amount}"
        self.stack -= amount
        self.currentBet = amount
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": message}})
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def bet(self, amount: int, previousAmount: int): # Throw si stack insuffisant ?
        self.stack -= amount + previousAmount - self.currentBet
        self.currentBet = previousAmount + amount
        if (previousAmount):
            message = f"Raises to {self.currentBet}"
        else:
            message = f"Bets {amount}"
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": message}})
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def call(self, amount: int):
        if (amount == 0):
            return self.check()
        self.currentBet += amount
        self.stack -= amount
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Calls {amount}"}})
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def fold(self):
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Folds"}})
        self.currentBet = 0
    def check(self):
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Checks"}})
    def win(self, amount: int):
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Wins {amount + self.currentBet}"}})
        self.stack += amount + self.currentBet
        self.currentBet = 0
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def loses(self):
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": "Loses"}})        

class Table():
    def __init__(self):
        super().__init__()
        self.P1 = Player("Joueur 1", 1)
        self.P2 = Player("Joueur 2", 2)
        self.players = [self.P1, self.P2]
        self.pot = 0
        self.board = []
        self.eq = [0.5, 0.5]
        self.actionOn = 1
        self.dealer = 1
        self.smallBlind = 1
        self.bigBlind = 2
        self.resetCards()
        self.changeDealer()
        self.sendAll()

    def changeDealer(self):
        self.dealer = (self.dealer + 1) % 2
        cl.send("SetInputSettings", {"inputName": f"P{self.dealer+1}dealer", "inputSettings": {"text": "BU"}})
        cl.send("SetInputSettings", {"inputName": f"P{(self.dealer+1)%2+1}dealer", "inputSettings": {"text": "BB"}})
        self.setAction(self.dealer)
    def setBoard(self, board: [str] = []):
        if len(board) > 5:
            raise CustomErr
        for i in range(len(board)):
            board[i] = fast_type(board[i])
            if not is_valid_card(board[i]):
                print(f"{board[i]} failed")
                raise CustomErr
        for i in range(5):
            if i < len(board):
                color = color_code[board[i][1]]
                cl.send("SetInputSettings", {"inputName": f"Board{i+1}", "inputSettings": {"text": board[i], "color": color}})
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id(f"Board{i+1}?", cl), "sceneItemEnabled": False})
            else:
                cl.send("SetInputSettings", {"inputName": f"Board{i+1}", "inputSettings": {"text": "?", "color": 0xffffff}})
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id(f"Board{i+1}?", cl), "sceneItemEnabled": True})
        self.board = board
    def resetCards(self):
        self.setBoard([])
        self.P1.setCards(["??", "??"])
        self.P2.setCards(["??", "??"])
        self.hideAll()
        cl.send("SetInputSettings", {"inputName": "EQ1", "inputSettings": {"text": "{0:.0f}%".format(0.5 * 100)}})
        cl.send("SetInputSettings", {"inputName": "EQ2", "inputSettings": {"text": "{0:.0f}%".format(0.5 * 100)}})
        self.pot = 0
        cl.send("SetInputSettings", {"inputName": "Pot", "inputSettings": {"text": f"Pot: {self.pot}"}})
    def setBlinds(self, small: int, big: int):
        self.smallBlind = small
        self.bigBlind = big
        cl.send("SetInputSettings", {"inputName": "Blinds", "inputSettings": {"text": f"{self.smallBlind}/{self.bigBlind}"}})
    def calcEq(self):
        if (valid_config(self.P1.cards, self.P2.cards, self.board)):
            cards = self.P1.cards + self.P2.cards
            board = self.board
            for i in range(4):
                cards[i] = un_fast_type(cards[i])
            for i in range(len(board)):
                board[i] = un_fast_type(board[i])
            self.eq = probas.get_eq(cards, board)
            cl.send("SetInputSettings", {"inputName": "EQ1", "inputSettings": {"text": "{0:.0f}%".format(self.eq[0] * 100)}})
            cl.send("SetInputSettings", {"inputName": "EQ2", "inputSettings": {"text": "{0:.0f}%".format(self.eq[1] * 100)}})
        else:
            raise CustomErr
    def sendAll(self):
        cl.send("SetInputSettings", {"inputName": "P1_name", "inputSettings": {"text": self.P1.name}})
        cl.send("SetInputSettings", {"inputName": "P2_name", "inputSettings": {"text": self.P2.name}})
        cl.send("SetInputSettings", {"inputName": "P1_stack", "inputSettings": {"text": str(self.P1.stack)}})
        cl.send("SetInputSettings", {"inputName": "P2_stack", "inputSettings": {"text": str(self.P2.stack)}})
        cl.send("SetInputSettings", {"inputName": "Blinds", "inputSettings": {"text": f"{self.smallBlind}/{self.bigBlind}"}})
        self.hideAll()
    def hideAll(self):
        try:
            resp = cl.send("GetSceneItemList", {"sceneName": "Scene"})
            l = []
            for item in resp.scene_items:
                if item["sourceName"].find("?") != -1:
                    l.append(item["sceneItemId"])
            for ids in l:
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": ids, "sceneItemEnabled": True})
        except Exception as e:
            print(e)
    def setAction(self, n: int):
        self.actionOn = (n + 1) % 2
        self.changeAction()
    def changeAction(self):
        id = get_item_id("ActionArrow", cl)
        self.actionOn = (self.actionOn + 1) % 2
        cl.send("SetSceneItemTransform", {"sceneName": "Scene", "sceneItemId": id, "sceneItemTransform": {"positionY": 110 + self.actionOn * 570}})
    def postBlinds(self):
        self.players[self.dealer].postBlinds(self.smallBlind, False)
        self.players[int(not self.dealer)].postBlinds(self.bigBlind, True)
    def call(self):
        if (len(self.board) == 0 and self.actionOn == self.dealer and self.players[int(not self.actionOn)].currentBet == self.bigBlind):
            self.players[self.actionOn].call(self.players[not int(self.actionOn)].currentBet - self.players[self.actionOn].currentBet)
            self.changeAction()
        elif len(self.board) != 0 and self.actionOn == int(not self.dealer) and not self.players[actionOn].currentBet:
            self.players[self.actionOn].check()
            self.changeAction()
        else:
            self.players[self.actionOn].call(self.players[not int(self.actionOn)].currentBet - self.players[self.actionOn].currentBet)
            self.pot = self.players[int(not self.actionOn)].currentBet * 2
            self.players[int(not self.actionOn)].currentBet = 0
            self.players[self.actionOn].currentBet = 0
            self.setAction(int(not self.dealer))
            cl.send("SetInputSettings", {"inputName": "Pot", "inputSettings": {"text": f"Pot: {self.pot}"}})
    def bet(self, amount: int):
        self.players[self.actionOn].bet(amount, self.players[int(not self.actionOn)].currentBet)
        self.changeAction()
    def fold(self):
        self.players[int(not self.actionOn)].win(self.pot + self.players[self.actionOn].currentBet)
        self.players[self.actionOn].fold()
        self.changeDealer()

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
            self.stack.setText(str(self.table.players[self.number].stack))
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
    def refresh(self):
        self.setEq()
        self.setCurrentBet()
        self.setCurrentStack()

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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Poker Stream Deck")
        self.table = Table()
        self.PlayersWidget = PlayersWidget(PlayerWidget(0, self.table), PlayerWidget(1, self.table))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputLine = QLineEdit(parent=self)

        buttonBoard = QPushButton("Set board", self)
        buttonBoard.clicked.connect(self.setBoard)
        buttondealer = QPushButton("Change Dealer", self)
        buttondealer.clicked.connect(self.table.changeDealer)
        buttonBlinds = QPushButton("Set blinds", self)
        buttonBlinds.clicked.connect(self.setBlinds)
        buttonReset = QPushButton("Reset cards", self)
        buttonReset.clicked.connect(self.resetCards)
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

        self.label = QLabel("Coucou toi")
        layout.addWidget(self.PlayersWidget)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(buttonBoard)
        layout.addWidget(buttondealer)
        layout.addWidget(buttonBlinds)
        layout.addWidget(buttonReset)
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
            if not valid_config(self.table.players[0].cards, self.table.players[1].cards, self.table.board):
                raise CustomErr
            self.table.setBoard(board)
            self.calcEq()
            self.label.setText("Successfully updated board")
        except Exception as e:
            print(e)
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
        self.P1Widget.refresh()
        self.P2Widget.refresh()
    def call(self):
        self.table.call()
        self.P1Widget.refresh()
        self.P2Widget.refresh()
    def bet(self):
        amount = self.inputLine.text()
        try:
            amount = int(amount)
            self.table.bet(amount)
            self.P1Widget.refresh()
            self.P2Widget.refresh()
        except Exception as e:
            print(e)
            self.label.setText("Error: Should be a positive number")
    def fold(self):
        self.table.fold()
        self.P1Widget.refresh()
        self.P2Widget.refresh()

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        cl = obs.ReqClient(host=keys.host, port=keys.port, password=keys.passw, timeout=3)
        window = Window()
        window.show()
        sys.exit(app.exec())
        cl.close()
    except Exception as e:
        print(e)
        print("Uh Oh")