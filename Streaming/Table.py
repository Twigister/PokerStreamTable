from Player import Player
from CustomErr import CustomErr
from utils import fast_type, is_valid_card, un_fast_type, get_item_id, color_code, valid_config
import options
import equity.probas as probas

import globalv
import communication

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
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.dealer+1}dealer", "inputSettings": {"text": "BU"}})
        globalv.cl.send("SetInputSettings", {"inputName": f"P{(self.dealer+1)%2+1}dealer", "inputSettings": {"text": "BB"}})
        self.setAction(self.dealer)
    def setBoard(self, board: list[str] = []):
        print(f"testing {board}")
        if len(board) > 5:
            raise CustomErr
        for i in range(len(board)):
            if (board[i]) != "??":
                board[i] = fast_type(board[i])
            if not (is_valid_card(board[i]) or board[i] == '??'):
                print(f"{board[i]} failed")
                raise CustomErr
        print("1st for ok")
        for i in range(5):
            if i < len(board) and board[i] != "??":
                color = color_code[board[i][1]]
                globalv.cl.send("SetInputSettings", {"inputName": f"Board{i+1}", "inputSettings": {"text": board[i], "color": color}})
                globalv.cl.send("SetSceneItemEnabled", {"sceneName": options.boardScene, "sceneItemId": get_item_id(f"Board{i+1}?", options.boardScene, globalv.cl), "sceneItemEnabled": False})
            else:
                globalv.cl.send("SetInputSettings", {"inputName": f"Board{i+1}", "inputSettings": {"text": "?", "color": 0xffffff}})
                globalv.cl.send("SetSceneItemEnabled", {"sceneName": options.boardScene, "sceneItemId": get_item_id(f"Board{i+1}?", options.boardScene, globalv.cl), "sceneItemEnabled": True})
        self.board = board
        print("Table.setBoard success")
    def resetCards(self):
        self.setBoard([])
        self.players[0].setCards()
        self.players[1].setCards()
        # self.hideAll()
        globalv.cl.send("SetInputSettings", {"inputName": "EQ1", "inputSettings": {"text": "{0:.0f}%".format(0.5 * 100)}})
        globalv.cl.send("SetInputSettings", {"inputName": "EQ2", "inputSettings": {"text": "{0:.0f}%".format(0.5 * 100)}})
        self.pot = 0
        globalv.cl.send("SetInputSettings", {"inputName": "Pot", "inputSettings": {"text": f"Pot: {self.pot}"}})
    def setBlinds(self, small: int, big: int):
        self.smallBlind = small
        self.bigBlind = big
        globalv.cl.send("SetInputSettings", {"inputName": "Blinds", "inputSettings": {"text": f"NLH {self.smallBlind}/{self.bigBlind}"}})
    def calcEq(self):
        if (valid_config(self.P1.cards, self.P2.cards, self.board)):
            cards = self.P1.cards + self.P2.cards
            board = self.board
            for i in range(4):
                cards[i] = un_fast_type(cards[i])
            for i in range(len(board)):
                board[i] = un_fast_type(board[i])
            self.eq = probas.get_eq(cards, board)
            globalv.cl.send("SetInputSettings", {"inputName": "EQ1", "inputSettings": {"text": "{0:.0f}%".format(self.eq[0] * 100)}})
            globalv.cl.send("SetInputSettings", {"inputName": "EQ2", "inputSettings": {"text": "{0:.0f}%".format(self.eq[1] * 100)}})
            globalv.cl.send("SetSceneItemEnabled", {"sceneName": options.playerScene[0], "sceneItemId": get_item_id("EQ1", options.playerScene[0], globalv.cl), "sceneItemEnabled": True})
            globalv.cl.send("SetSceneItemEnabled", {"sceneName": options.playerScene[1], "sceneItemId": get_item_id("EQ2", options.playerScene[1], globalv.cl), "sceneItemEnabled": True})
        else:
            raise CustomErr("Cul")
    def hideEq(self):
        globalv.cl.send("SetSceneItemEnabled", {"sceneName": options.playerScene[0], "sceneItemId": get_item_id("EQ1", options.playerScene[0], globalv.cl), "sceneItemEnabled": False})
        globalv.cl.send("SetSceneItemEnabled", {"sceneName": options.playerScene[1], "sceneItemId": get_item_id("EQ2", options.playerScene[1], globalv.cl), "sceneItemEnabled": False})
    def sendAll(self):
        globalv.cl.send("SetInputSettings", {"inputName": "P1_name", "inputSettings": {"text": self.P1.name}})
        globalv.cl.send("SetInputSettings", {"inputName": "P2_name", "inputSettings": {"text": self.P2.name}})
        globalv.cl.send("SetInputSettings", {"inputName": "P1_stack", "inputSettings": {"text": str(self.P1.stack)}})
        globalv.cl.send("SetInputSettings", {"inputName": "P2_stack", "inputSettings": {"text": str(self.P2.stack)}})
        globalv.cl.send("SetInputSettings", {"inputName": "Blinds", "inputSettings": {"text": f"NLH {self.smallBlind}/{self.bigBlind}"}})
        self.hideAll()
    def hideAll(self):
        try:
            resp = globalv.cl.send("GetSceneItemList", {"sceneName": "Scene"})
            l = []
            for item in resp.scene_items:
                if item["sourceName"].find("?") != -1:
                    l.append(item["sceneItemId"])
            for ids in l:
                globalv.cl.send("SetSceneItemEnabled", {"sceneName": "Scene", "sceneItemId": ids, "sceneItemEnabled": True})
            self.hideEq()
        except Exception as e:
            print(e)
    def setAction(self, n: int):
        self.actionOn = (n + 1) % 2
        self.changeAction()
    def changeAction(self):
        id = get_item_id("ActionArrow", options.MainSceneName, globalv.cl)
        self.actionOn = (self.actionOn + 1) % 2
        globalv.cl.send("SetSceneItemTransform", {"sceneName": "Scene", "sceneItemId": id, "sceneItemTransform": {"positionX": 204 + self.actionOn * 1483}})
    def postBlinds(self):
        self.players[self.dealer].postBlinds(self.smallBlind, False)
        self.players[int(not self.dealer)].postBlinds(self.bigBlind, True)
    def call(self):
        if (len(self.board) == 0 and self.actionOn == self.dealer and self.players[int(not self.actionOn)].currentBet == self.bigBlind):
            self.players[self.actionOn].call(self.players[not int(self.actionOn)].currentBet - self.players[self.actionOn].currentBet)
            self.changeAction()
        elif len(self.board) != 0 and self.actionOn == int(not self.dealer) and not self.players[self.actionOn].currentBet:
            self.players[self.actionOn].check()
            self.changeAction()
        else:
            self.players[self.actionOn].call(self.players[not int(self.actionOn)].currentBet - self.players[self.actionOn].currentBet)
            self.pot += self.players[int(not self.actionOn)].currentBet * 2
            self.players[int(not self.actionOn)].currentBet = 0
            self.players[self.actionOn].currentBet = 0
            self.setAction(int(not self.dealer))
            globalv.cl.send("SetInputSettings", {"inputName": "Pot", "inputSettings": {"text": f"Pot: {self.pot}"}})
            if (len(self.board) == 5):
                for i in range(2):
                    if self.eq[i] == 1:
                        self.players[i].win(self.pot)
                    elif self.eq[i] == 0.5:
                        self.players[i].win(self.pot / 2)
                    else:
                        self.players[i].loses()
    def bet(self, amount: int):
        self.players[self.actionOn].bet(amount, self.players[int(not self.actionOn)].currentBet)
        self.changeAction()
    def fold(self):
        self.players[int(not self.actionOn)].win(self.pot + self.players[self.actionOn].currentBet)
        self.players[self.actionOn].fold()
        self.changeDealer()
    def newHand(self):
        self.changeDealer()
        self.setBoard()
        for player in self.players:
            player.setCards()
            self.hideEq()
        self.postBlinds()
    def setCard(self, player: int, cardno: int, card: str):
        tempcards = self.players[player].cards
        tempcards[cardno] = fast_type(card)
        if (tempcards.count("??")):
            tempcards = tempcards.remove("??")
        tempcards2 = self.players[(player + 1) % 2].cards
        if (tempcards2.count("??")):
            tempcards2 = tempcards2.remove("??")
        if tempcards2 == None:
            tempcards2 = []
        if valid_config(tempcards, tempcards2, self.board):
            self.players[player].setCard(cardno, card)
            self.calcEq()
