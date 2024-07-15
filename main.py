from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
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
        self.cards = ["?", "?"]
    def setName(self, name: str):
        self.name = name
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_name", "inputSettings": {"text": name}})
    def setStack(self, stack: int):
        self.stack = stack
        self.deposit = stack
        cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(stack)}})
    def setCards(self, cards: [str, str] = ["?", "?"]):
        self.cards = cards
        for i in range(2):
            card = cards[i]
            if (card == "?"):
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
        print(self.stack)
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
        self.actionOn = 1
        self.dealer = 1
        self.smallBlind = 1
        self.bigBlind = 2
        self.resetCards()
        self.changeDealer()
        self.sendAll()

    # Setters
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
        self.P1.setCards(["?", "?"])
        self.P2.setCards(["?", "?"])
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
            eq = probas.get_eq(cards, board)
            cl.send("SetInputSettings", {"inputName": "EQ1", "inputSettings": {"text": "{0:.0f}%".format(eq[0] * 100)}})
            cl.send("SetInputSettings", {"inputName": "EQ2", "inputSettings": {"text": "{0:.0f}%".format(eq[1] * 100)}})
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
        if (len(self.board) == 0 and self.actionOn == self.dealer and self.players[int(not self.actionOn)].currentBet != self.bigBlind):
            self.players[self.actionOn].call(self.players[not int(self.actionOn)].currentBet - self.players[self.actionOn].currentBet)
            self.changeAction()
        elif len(self.board) != 0 and self.ActionArrow == int(not self.dealer) and not self.players[actionOn].currentBet:
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


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("Poker Stream Deck")
        self.table = Table()
        # self.setWindowIcon(QIcon("coucou.jpg"))

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.inputLine = QLineEdit(parent=self)

        buttonNameP1 = QPushButton("Set P1 name", self)
        buttonNameP1.clicked.connect(self.changeP1Name)
        buttonStackP1 = QPushButton("Set P1 stack", self)
        buttonStackP1.clicked.connect(self.setP1stack)        
        buttonAddonP1 = QPushButton("Addon P1", self)
        buttonAddonP1.clicked.connect(self.addonP1)
        buttonNameP2 = QPushButton("Set P2 name", self)
        buttonNameP2.clicked.connect(self.changeP2Name)
        buttonStackP2 = QPushButton("Set P2 stack", self)
        buttonStackP2.clicked.connect(self.setP2stack)
        buttonAddonP2 = QPushButton("Addon P2", self)
        buttonAddonP2.clicked.connect(self.addonP2)
        buttonboard = QPushButton("Set board", self)
        buttonboard.clicked.connect(self.setBoard)
        buttoncards1 = QPushButton("Set P1 cards", self)
        buttoncards1.clicked.connect(self.setP1Cards)
        buttoncards2 = QPushButton("Set P2 cards", self)
        buttoncards2.clicked.connect(self.setP2Cards)
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
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(buttonNameP1)
        layout.addWidget(buttonStackP1)
        layout.addWidget(buttonAddonP1)
        layout.addWidget(buttonNameP2)
        layout.addWidget(buttonStackP2)
        layout.addWidget(buttonAddonP2)
        layout.addWidget(buttonboard)
        layout.addWidget(buttoncards1)
        layout.addWidget(buttoncards2)
        layout.addWidget(buttondealer)
        layout.addWidget(buttonBlinds)
        layout.addWidget(buttonReset)
        layout.addWidget(buttonEQ)
        layout.addWidget(buttonPostBlinds)
        layout.addWidget(buttonCall)
        layout.addWidget(buttonBet)
        layout.addWidget(buttonFold)
        layout.addWidget(self.inputLine)

        self.P1name = QLabel(self.table.P1.name)
        self.P2name = QLabel(self.table.P2.name)
        self.P1stack = QLabel(str(self.table.P1.stack))
        self.P2stack = QLabel(str(self.table.P2.stack))
        self.P1cards = QLabel(str(self.table.P1.cards))
        self.P2cards = QLabel(str(self.table.P2.cards))
        layout.addWidget(self.P1name)
        layout.addWidget(self.P1stack)
        layout.addWidget(self.P1cards)
        layout.addWidget(self.P2name)
        layout.addWidget(self.P2stack)
        layout.addWidget(self.P2cards)

    def changeP1Name(self):
        self.table.P1.setName(self.inputLine.text())
        self.label.setText(f"Changed P1 name to: {self.table.P1.name}")
        self.P1name.setText(self.table.P1.name)
    def changeP2Name(self):
        self.table.P2.setName(self.inputLine.text())
        self.label.setText(f"Changed P2 name to: {self.table.P2.name}")
        self.P2name.setText(self.table.P2.name)
    def setP1stack(self):
        try:
            value = int(self.inputLine.text())
            self.table.P1.setStack(value)
            self.label.setText(f"Changed P1 stack to {self.table.P1.stack}")
            self.P1stack.setText(str(self.table.P1.stack))
        except:
            self.label.setText("Error: Must be an integer value")
    def setP2stack(self):
        try:
            value = int(self.inputLine.text())
            self.table.P2.setStack(value)
            self.label.setText(f"Changed P2 stack to {self.table.P2.stack}")
            self.P2stack.setText(str(self.table.P2.stack))
        except:
            self.label.setText("Error: Must be an integer value")
    def addonP1(self):
        try:
            value = int(self.inputLine.text())
            if (value <= 0):
                raise Exception()                
            self.table.P1.addon(value)
            self.label.setText(f"Addon {value} to {self.table.P1.stack}")
            self.P1stack.setText(str(self.table.P1.stack))
        except:
            self.label.setText("Error: Must be an integer value")
    def addonP2(self):
        try:
            value = int(self.inputLine.text())
            if (value <= 0):
                raise Exception()
            self.table.P2.addon(value)
            self.label.setText(f"Addon {value} to {self.table.P2.stack}")
            self.P2stack.setText(str(self.table.P2.stack))
        except:
            self.label.setText("Error: Must be an integer value")
    def setBoard(self):
        try:
            if (self.inputLine.text() != ""):
                board = self.inputLine.text().split(" ")
            else:
                board = []
            self.table.setBoard(board)
            self.label.setText("Successfully updated board")
        except Exception as e:
            print(e)
            self.label.setText("Error: Invalid cards")
    def setP1Cards(self):
        cards = self.inputLine.text().split(" ")
        if (len(cards) != 2):
            self.label.setText("Error: number of cards invalid")
        else:
            for i in range(2):
                cards[i] = fast_type(cards[i])
            try:
                self.table.P1.setCards(cards)
                self.label.setText("P1 cards update Success")
                self.P1cards.setText(str(cards))
            except Exception as e:
                print(e)
                self.label.setText("Error: Invalid card")
    def setP2Cards(self):
        cards = self.inputLine.text().split(" ")
        if (len(cards) != 2):
            self.label.setText("Error: number of cards invalid")
        else:
            for i in range(2):
                cards[i] = fast_type(cards[i])
            try:
                self.table.P2.setCards(cards)
                self.label.setText("P2 cards update Success")
                self.P2cards.setText(str(cards))
            except Exception as e:
                print(e)
                self.label.setText("Error: Invalid card")
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
        except:
            self.label.setText("Error in eq calculation")
    def postBlinds(self):
        self.table.postBlinds()
    def call(self):
        self.table.call()
    def bet(self):
        amount = self.inputLine.text()
        # try:
        amount = int(amount)
        self.table.bet(amount)
        # except Exception as e:
        #     print(e)
        #     self.label.setText("Error: Should be a positive number")
    def fold(self):
        self.table.fold()

if __name__ == "__main__":
    # try:
        app = QApplication(sys.argv)
        cl = obs.ReqClient(host=keys.host, port=keys.port, password=keys.passw, timeout=3)
        window = Window()
        window.show()
        sys.exit(app.exec())
        cl.close()
    # except Exception as e:
    #     print(e)
    #     print("Uh Oh")