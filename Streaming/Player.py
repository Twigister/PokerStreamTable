from utils import *
import options
import globalv

class Player():
    def __init__(self, name: str, number: int):
        super().__init__()
        self.name = name
        self.number = number
        self.stack = 0
        self.currentBet = 0
        self.deposit = 0
        self.cards = ["??", "??"]
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": "Sat in"}})
    def setName(self, name: str):
        self.name = name
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_name", "inputSettings": {"text": name}})
    def setStack(self, stack: int):
        self.stack = stack
        self.deposit = stack
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(stack)}})
    def setCards(self, cards: list[str] = ["??", "??"]):
        self.cards = cards
        for i in range(2):
            card = cards[i]
            sceneName = options.playerScene[self.number - 1]
            sourceName = f"Carte{self.number}-{i + 1}"
            if (card == "??"):
                globalv.cl.send("SetInputSettings", {"inputName": sourceName, "inputSettings": {"text": "??", "color": 0}})
                globalv.cl.send("SetSceneItemEnabled", {"sceneName": sceneName, "sceneItemId": get_item_id(f"{sourceName}?", sceneName, globalv.cl), "sceneItemEnabled": True})
            elif is_valid_card(card):
                globalv.cl.send("SetInputSettings", {"inputName": sourceName, "inputSettings": {"text": cards[i], "color": color_code[cards[i][1]]}})
                globalv.cl.send("SetSceneItemEnabled", {"sceneName": sceneName, "sceneItemId": get_item_id(f"{sourceName}?", sceneName, globalv.cl), "sceneItemEnabled": False})
            else:
                return self.setCards()
    def addon(self, amount: int):
        self.stack += amount
        self.deposit += amount
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def postBlinds(self, amount: int, isBB: bool):
        if isBB:
            message = f"Posts BB: {amount}"
        else:
            message = f"Posts SB: {amount}"
        self.stack -= amount
        self.currentBet = amount
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": message}})
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def bet(self, amount: int, previousAmount: int): # Throw si stack insuffisant ?
        self.stack -= amount + previousAmount - self.currentBet
        self.currentBet = previousAmount + amount
        if (previousAmount):
            message = f"Raises to {self.currentBet}"
        else:
            message = f"Bets {amount}"
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": message}})
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def call(self, amount: int):
        if (amount == 0):
            return self.check()
        self.currentBet += amount
        self.stack -= amount
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Calls {amount}"}})
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def fold(self):
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Folds"}})
        self.currentBet = 0
    def check(self):
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Checks"}})
    def win(self, amount: int):
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": f"Wins {amount + self.currentBet}"}})
        self.stack += amount + self.currentBet
        self.currentBet = 0
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_stack", "inputSettings": {"text": str(self.stack)}})
    def loses(self):
        globalv.cl.send("SetInputSettings", {"inputName": f"P{self.number}_action", "inputSettings": {"text": "Loses"}})
    def setCard(self, cardno: int, card: str):
        self.cards[cardno] = fast_type(card)
        print("Calling Player.setCard")
        sceneName = options.playerScene[self.number - 1]
        print(f"Modifying: {sceneName}")
        sourceName = f"Carte{self.number}-{cardno + 1}"
        print(f"Source name: {sourceName}")
        if is_valid_card(self.cards[cardno]):
            print("Card is valid")
            globalv.cl.send("SetInputSettings", {"inputName": sourceName, "inputSettings": {"text": self.cards[cardno], "color": color_code[self.cards[cardno][1]]}})
            print("Text correctly changed")
            globalv.cl.send("SetSceneItemEnabled", {"sceneName": sceneName, "sceneItemId": get_item_id(f"{sourceName}?", sceneName, globalv.cl), "sceneItemEnabled": False})
            print("Card back unloaded")
        else:
            print("coucou ca marche pas")
