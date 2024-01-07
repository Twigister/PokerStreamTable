import envoi_cartes
import probas
import obswebsocket
import keys

import threading

board = []
cards = ["", "", "", ""]
button = 0

def	cards_are_valid(cards, board):
	if len(cards) != 4:
		return False
	all = cards + board
	comp = set(all)
	if len(all) != len(comp):
		return False
	for card in all:
		if (envoi_cartes.is_valid_card(envoi_cartes.fast_type(card)) == False):
			return False
	return True

def reset(socket):
    global board 
    global cards

    board = []
    cards = ["", "", "", ""]
    envoi_cartes.hide_everything(socket)

def eq_calc():
    global board
    global cards

    res = probas.get_eq(cards, [])
    print("Preflop EQ: {0} {1}".format(res[0], res[1]))
    if (len(board) == 0):
        envoi_cartes.change_text(socket, 1, envoi_cartes.fast_type("{0} {1}".format(cards[0], cards[1])), res[0])
        envoi_cartes.change_text(socket, 2, envoi_cartes.fast_type("{0} {1}".format(cards[2], cards[3])), res[1])

def get_cards(socket):
	p1_cards = input("Please enter P1 cards: ")
	tmp = p1_cards.split()
	if (len(tmp) == 2):
		p1_cards = tmp
	print(p1_cards)
    
	p2_cards = input("Please enter P2 cards: ")
	tmp = p2_cards.split()
	if (len(tmp) == 2):
		p2_cards = tmp
	print(p2_cards)
    
	global cards
	cards = p1_cards + p2_cards
	envoi_cartes.change_text(socket, 1, envoi_cartes.fast_type("{0} {1}".format(cards[0], cards[1])), -1)
	envoi_cartes.change_text(socket, 2, envoi_cartes.fast_type("{0} {1}".format(cards[2], cards[3])), -1)
	if (cards_are_valid(cards, [])):
		thread = threading.Thread(target=eq_calc)
		thread.daemon = True
		thread.start()

def get_flop(socket):
	global board
	global cards
	flop = ["9h", "Th", "2d"]
	board = flop.copy()
	for i in range(len(flop)):
		flop[i] = envoi_cartes.fast_type(flop[i])
	envoi_cartes.set_flop(socket, flop)
	if cards_are_valid(cards, board):
		res = probas.get_eq(cards, board)
		envoi_cartes.set_eq(socket, 1, res[0])
		envoi_cartes.set_eq(socket, 2, res[1])
	else:
		print("Invalid cards ?")
def get_turn(socket):
	global cards
	global board

	turn = "Jh"
	board.append(turn)
	turn = envoi_cartes.fast_type(turn)
	envoi_cartes.set_turn(socket, turn)
	if cards_are_valid(cards, board):
		res = probas.get_eq(cards, board)
		envoi_cartes.set_eq(socket, 1, res[0])
		envoi_cartes.set_eq(socket, 2, res[1])

def get_river(socket):
	global cards
	global board

	river = "Ah"
	board.append(river)
	river = envoi_cartes.fast_type(river)
	envoi_cartes.set_river(socket, river)
	if cards_are_valid(cards, board):
		res = probas.get_eq(cards, board)
		envoi_cartes.set_eq(socket, 1, res[0])
		envoi_cartes.set_eq(socket, 2, res[1])

def	set_player_names(socket):
	name1 = input("P1 name: ")
	name2 = input("P2 name: ")
	envoi_cartes.set_player_names(socket, name1, name2)

def reset_board(socket):
    global board
    board = []
    envoi_cartes.hide_everything(socket)

commands = {"hide": envoi_cartes.hide_everything,
            "get_cards": get_cards,
            "get_flop": get_flop,
            "get_turn": get_turn,
            "get_river": get_river,
            "reset": reset,
			"set_player_names": set_player_names
			}
def run_command(command, socket):
    command = command.split()
    if command[0] in commands:
        commands[command[0]](socket)
    else:
        print("Invalid command")

if __name__ == "__main__":
	socket = obswebsocket.obsws(keys.host, keys.port, keys.passw)
	socket.connect()
	while (1):
		command = input("$> ")
		if (command == "exit"):
			break
		run_command(command, socket)
	socket.disconnect()