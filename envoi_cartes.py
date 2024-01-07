import obswebsocket
from obswebsocket import requests as obs_requests
import keys

color_code = { "♣": 0x00ff00, "♦": 0xfffb00, "♥": 0x0000ff, "♠": 0x000000 }

def get_object_id(socket, source_name):
    scene = socket.call(obs_requests.GetSceneItemList())
    items = scene.datain['sceneItems']

    print(items)
    item_id = -1
    for item in items:
        if item['sourceName'] == source_name:
            item_id = item['itemId']
            break
    return item_id

def toggle_source_visibility(socket, source_name, visibility):
    socket.call(obs_requests.SetSceneItemProperties(**{"scene" : "Scene", "item": source_name, "visible": visibility}))
                
def hide_everything(socket):
        sources = []

        for i in range(2):
                for j in range(2):
                        source = f"Carte{i+1}-{j+1}"
                        sources.append(source)
                source = f"EQ{i+1}"
                sources.append(source)
        for i in range(3):
                source = f"Flop{i+1}"
                sources.append(source)
        sources.append("Turn")
        sources.append("River")
        for e in sources:
            res = toggle_source_visibility(socket, e, False)

def set_eq(socket, player, eq):
        text = "{0:.0f}%".format(eq * 100)
        source = f"EQ{player}"
        req = {"source": source, "text": text}
        socket.call(obs_requests.SetTextGDIPlusProperties(**req))
        toggle_source_visibility(socket, source, True)

def change_text(socket, player, cards, eq):
        card_data = cards.split()

        for i in range(len(card_data)):
                color = color_code[(card_data[i])[-1]]
                text = card_data[i]
                source = f"Carte{player}-{1+i}"
                req = {"source": source, "text": text, "color": color }
                socket.call(obs_requests.SetTextGDIPlusProperties(**req))
                toggle_source_visibility(socket, source, True)
        if (eq != -1):
                set_eq(socket, player, eq)

def set_flop(socket, cards):
        for i in range(len(cards)):
                color = color_code[(cards[i])[1]]
                text = cards[i]
                source = f"Flop{i+1}"
                req = {"source": source, "text": text, "color": color }
                socket.call(obs_requests.SetTextGDIPlusProperties(**req))
                toggle_source_visibility(socket, source, True)

def set_turn(socket, card):
        color = color_code[card[1]]
        text = card
        source = f"Turn"
        req = {"source": source, "text": text, "color": color }
        socket.call(obs_requests.SetTextGDIPlusProperties(**req))
        toggle_source_visibility(socket, source, True)

def set_river(socket, card):
        color = color_code[card[1]]
        text = card
        source = f"River"
        req = {"source": source, "text": text, "color": color }
        socket.call(obs_requests.SetTextGDIPlusProperties(**req))
        toggle_source_visibility(socket, source, True)

def fast_type(cards):
	cards = cards.replace("h", "♥")
	cards = cards.replace("s", "♠")
	cards = cards.replace("d", "♦")
	cards = cards.replace("c", "♣")
	return cards

if __name__ == "__main__":
        host = keys.host
        port = keys.port
        passw = keys.passw
        # ♣♦♥♠
        socket = obswebsocket.obsws(host, port, passw)
        socket.connect()

        #text_data = { "text": "A♠ A♣", "source": "Carte1" }

        #socket.call(obs_requests.SetTextGDIPlusProperties(**text_data))
        
        change_text(socket, 1, fast_type("Jh 7d"), .50)
        change_text(socket, 2, fast_type("Js 7c"), .50)

        socket.disconnect()
