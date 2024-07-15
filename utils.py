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
def get_item_id(name: str, cl):
    resp = cl.send("GetSceneItemList", {"sceneName": "Scene"})
    for item in resp.scene_items:
        if item["sourceName"] == name:
            return item["sceneItemId"]
