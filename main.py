from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import sys
import keys
import probas
import obsws_python as obs
color_code = { "♣": 0x268500, "♦": 0x911147, "♥": 0x0000ff, "♠": 0x000000 }
# color_code = { "♣": 0x268500, "♦": 0x910500, "♥": 0x0000ff, "♠": 0x000000 }
# color_code = { "♣": 0x00ff00, "♦": 0xfffb00, "♥": 0x0000ff, "♠": 0x000000 }
def fast_type(cards):
	cards = cards.replace("h", "♥")
	cards = cards.replace("s", "♠")
	cards = cards.replace("d", "♦")
	cards = cards.replace("c", "♣")
	return cards
def un_fast_type(cards):
    cards = cards.replace("♥", "h")
    cards = cards.replace("♠", "s")
    cards = cards.replace("♦", "d")
    cards = cards.replace("♣", "c")
    return cards
def	is_valid_card(card):
	value = "" + card[0]
	suit = "" + card[1]
	if (len(card) == 2 and "A23456789TJQK".find(value) != -1 and "♣♦♥♠".find(suit) != -1):
		return True
	else:
		return False

def valid_config(p1, p2, board):
    #TODO
    return True

def get_item_id(name: str):
    resp = cl.send("GetSceneItemList", {"sceneName": "Scene"})
    for item in resp.scene_items:
        if item["sourceName"] == name:
            return item["sceneItemId"]

class Table():
    def __init__(self):
        super().__init__()
        self.P1 = {"name": "Joueur 1", "stack": 0, "cards": ["?", "?"]}
        self.P2 = {"name": "Joueur 2", "stack": 0, "cards": ["?", "?"]}
        self.board = []
        self.dealer = 1
        self.smallBlind = 1
        self.bigBlind = 2
        self.resetCards()
        self.changeDealer()
        self.sendAll()

    # Setters
    def setP1Name(self, name):
        self.P1["name"] = name
        cl.send("SetInputSettings", {"inputName": "P1_name", "inputSettings": {"text": name}})
    def setP2Name(self, name):
        self.P2["name"] = name
        cl.send("SetInputSettings", {"inputName": "P2_name", "inputSettings": {"text": name}})
    def setP1Stack(self, stack):
        self.P1["stack"] = stack
        cl.send("SetInputSettings", {"inputName": "P1_stack", "inputSettings": {"text": str(stack)}})
    def setP2Stack(self, stack):
        self.P2["stack"] = stack
        cl.send("SetInputSettings", {"inputName": "P2_stack", "inputSettings": {"text": str(stack)}})
    def setP1Cards(self, cards: [str] = ["?", "?"]):
        self.P1["cards"] = cards
        if cards[0] == "?":
            cl.send("SetInputSettings", {"inputName": "Carte1-1", "inputSettings": {"text": "??", "color": 0}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte1-1?"), "sceneItemEnabled": True})
        elif is_valid_card(cards[0]):
            cl.send("SetInputSettings", {"inputName": "Carte1-1", "inputSettings": {"text": cards[0], "color": color_code[cards[0][1]]}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte1-1?"), "sceneItemEnabled": False})
        else:
            self.setP1Cards()
            raise CustomErr
        if (cards[1] == "?"):
            cl.send("SetInputSettings", {"inputName": "Carte1-2", "inputSettings": {"text": "??", "color": 0}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte1-2?"), "sceneItemEnabled": True})
        elif is_valid_card(cards[1]):
            cl.send("SetInputSettings", {"inputName": "Carte1-2", "inputSettings": {"text": cards[1], "color": color_code[cards[1][1]]}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte1-2?"), "sceneItemEnabled": False})
        else:
            self.setP1Cards()
            raise CustomErr
    def setP2Cards(self, cards: [str] = ["?", "?"]):
        self.P2["cards"] = cards
        if cards[0] == "?":
            cl.send("SetInputSettings", {"inputName": "Carte2-1", "inputSettings": {"text": "??", "color": 0}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte2-1?"), "sceneItemEnabled": True})
        elif is_valid_card(cards[0]):
            cl.send("SetInputSettings", {"inputName": "Carte2-1", "inputSettings": {"text": cards[0], "color": color_code[cards[0][1]]}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte2-1?"), "sceneItemEnabled": False})
        else:
            self.setP2Cards()
            raise CustomErr
        if (cards[1] == "?"):
            cl.send("SetInputSettings", {"inputName": "Carte2-2", "inputSettings": {"text": "??", "color": 0}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte2-2?"), "sceneItemEnabled": True})
        elif is_valid_card(cards[1]):
            cl.send("SetInputSettings", {"inputName": "Carte2-2", "inputSettings": {"text": cards[1], "color": color_code[cards[1][1]]}})
            cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id("Carte2-2?"), "sceneItemEnabled": False})
        else:
            self.setP2Cards()
            raise CustomErr
    def addonP1(self, amount):
        self.P1["stack"] += amount
        cl.send("SetInputSettings", {"inputName": "P1_stack", "inputSettings": {"text": str(self.P1["stack"])}})
    def addonP2(self, amount):
        self.P2["stack"] += amount
        cl.send("SetInputSettings", {"inputName": "P2_stack", "inputSettings": {"text": str(self.P2["stack"])}})
    def changeDealer(self):
        self.dealer = (self.dealer + 1) % 2
        cl.send("SetInputSettings", {"inputName": f"P{self.dealer+1}dealer", "inputSettings": {"text": "BU"}})
        cl.send("SetInputSettings", {"inputName": f"P{(self.dealer+1)%2+1}dealer", "inputSettings": {"text": "BB"}})

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
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id(f"Board{i+1}?"), "sceneItemEnabled": False})
            else:
                cl.send("SetInputSettings", {"inputName": f"Board{i+1}", "inputSettings": {"text": "?", "color": 0xffffff}})
                cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": get_item_id(f"Board{i+1}?"), "sceneItemEnabled": True})
        self.board = board
    def resetCards(self):
        self.setBoard([])
        self.setP1Cards(["?", "?"])
        self.setP2Cards(["?", "?"])
        self.hideAll()
        cl.send("SetInputSettings", {"inputName": "EQ1", "inputSettings": {"text": "{0:.0f}%".format(0.5 * 100)}})
        cl.send("SetInputSettings", {"inputName": "EQ2", "inputSettings": {"text": "{0:.0f}%".format(0.5 * 100)}})
    def setBlinds(self, small: int, big: int):
        self.smallBlind = small
        self.bigBlind = big
        cl.send("SetInputSettings", {"inputName": "Blinds", "inputSettings": {"text": f"{self.smallBlind}/{self.bigBlind}"}})
    def calcEq(self):
        if (valid_config(self.P1["cards"], self.P2["cards"], self.board)):
            cards = self.P1["cards"] + self.P2["cards"]
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
        cl.send("SetInputSettings", {"inputName": "P1_name", "inputSettings": {"text": self.P1["name"]}})
        cl.send("SetInputSettings", {"inputName": "P2_name", "inputSettings": {"text": self.P2["name"]}})
        cl.send("SetInputSettings", {"inputName": "P1_stack", "inputSettings": {"text": str(self.P1["stack"])}})
        cl.send("SetInputSettings", {"inputName": "P2_stack", "inputSettings": {"text": str(self.P2["stack"])}})
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

        button = QPushButton("Set P1 name", self)
        button.clicked.connect(self.changeP1Name)
        button2 = QPushButton("Set P1 stack", self)
        button2.clicked.connect(self.setP1stack)        
        button3 = QPushButton("Set P2 name", self)
        button3.clicked.connect(self.changeP2Name)
        button4 = QPushButton("Set P2 stack", self)
        button4.clicked.connect(self.setP2stack)
        button5 = QPushButton("Addon P1", self)
        button5.clicked.connect(self.addonP1)
        button6 = QPushButton("Addon P2", self)
        button6.clicked.connect(self.addonP2)
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

        self.label = QLabel("Coucou toi")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        layout.addWidget(button)
        layout.addWidget(button2)
        layout.addWidget(button3)
        layout.addWidget(button4)
        layout.addWidget(button5)
        layout.addWidget(button6)
        layout.addWidget(buttonboard)
        layout.addWidget(buttoncards1)
        layout.addWidget(buttoncards2)
        layout.addWidget(buttondealer)
        layout.addWidget(buttonBlinds)
        layout.addWidget(buttonReset)
        layout.addWidget(buttonEQ)
        layout.addWidget(self.inputLine)

        self.P1name = QLabel(self.table.P1["name"])
        self.P2name = QLabel(self.table.P2["name"])
        self.P1stack = QLabel(str(self.table.P1["stack"]))
        self.P2stack = QLabel(str(self.table.P2["stack"]))
        self.P1cards = QLabel(str(self.table.P1["cards"]))
        self.P2cards = QLabel(str(self.table.P2["cards"]))
        layout.addWidget(self.P1name)
        layout.addWidget(self.P2name)
        layout.addWidget(self.P1stack)
        layout.addWidget(self.P2stack)
        layout.addWidget(self.P1cards)
        layout.addWidget(self.P2cards)

    def changeP1Name(self):
        self.table.setP1Name(self.inputLine.text())
        self.label.setText(f"Changed P1 name to: {self.table.P1["name"]}")
        self.P1name.setText(self.table.P1["name"])
    def changeP2Name(self):
        self.table.setP2Name(self.inputLine.text())
        self.label.setText(f"Changed P2 name to: {self.table.P2["name"]}")
        self.P2name.setText(self.table.P2["name"])
    def setP1stack(self):
        try:
            value = int(self.inputLine.text())
            self.table.setP1Stack(value)
            self.label.setText(f"Changed P1 stack to {self.table.P1["stack"]}")
            self.P1stack.setText(str(value))
        except:
            self.label.setText("Error: Must be an integer value")
    def setP2stack(self):
        try:
            value = int(self.inputLine.text())
            self.table.setP2Stack(value)
            self.label.setText(f"Changed P2 stack to {self.table.P2["stack"]}")
            self.P2stack.setText(str(value))
        except:
            self.label.setText("Error: Must be an integer value")
    def addonP1(self):
        try:
            value = int(self.inputLine.text())
            self.table.addonP1(value)
            self.label.setText(f"Addon {value} to {self.table.P1["stack"]}")
            self.P1stack.setText(str(self.table.P1["stack"]))
        except:
            self.label.setText("Error: Must be an integer value")
    def addonP2(self):
        try:
            value = int(self.inputLine.text())
            self.table.addonP2(value)
            self.label.setText(f"Addon {value} to {self.table.P2["stack"]}")
            self.P2stack.setText(str(self.table.P2["stack"]))
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
            self.label.setText("Error: Invalid cards")
    def setP1Cards(self):
        cards = self.inputLine.text().split(" ")
        if (len(cards) != 2):
            self.label.setText("Error: number of cards invalid")
        else:
            for i in range(2):
                cards[i] = fast_type(cards[i])
            try:
                self.table.setP1Cards(cards)
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
                self.table.setP2Cards(cards)
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

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        cl = obs.ReqClient(host=keys.host, port=keys.port, password=keys.passw, timeout=3)
        window = Window()
        window.show()
        sys.exit(app.exec())
        cl.close()
    except:
        print("Uh Oh")