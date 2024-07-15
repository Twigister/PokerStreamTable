from options import color_code

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
    l = p1 + p2 + board
    for card in l:
        if not is_valid_card(card):
            return False
    if (len(l) != len(set(l))):
        return False
    return True
def get_item_id(name: str, sceneName: str, cl):
    resp = cl.send("GetSceneItemList", {"sceneName": sceneName})
    for item in resp.scene_items:
        if item["sourceName"] == name:
            return item["sceneItemId"]

