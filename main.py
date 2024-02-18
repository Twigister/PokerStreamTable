import envoi_cartes
import probas
import obswebsocket
import keys

import threading

board = []
cards = ["", "", "", ""]
button = 0
player1 = {
	"name": "Joueur 1",
	"stack": 100,
	"is_dealer": False,
	"last_bet": 0
	}

player2 = {
	"name": "Joueur 2",
	"stack": 100,
	"is_dealer": False
	"last_bet": 0
	}

blinds = [5, 10]

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
	global player1
	global player2

	name1 = input("P1 name: ")
	name2 = input("P2 name: ")
	envoi_cartes.set_player_names(socket, name1, name2)
	player1["name"] = name1
	player2["name"] = name2

def set_dealer(socket):
	global player1
	global player2

	while (1):
		dealer = input("Who should be dealing?")
		try:
			dealer = int(dealer)
			if (dealer == 1)
				player1["is_dealer"] = True
				player2["is_dealer"] = False
			else if (dealer == 2)
				player1["is_dealer"] = False
				player2["is_dealer"] = True
			else
				raise CustomErr("Test")
		except ValueError:
			print("Error: Not a number, please try again")
		except CustomErr:
				print("Value should either be 1 or 2")
		else:
			break;
	envoi_cartes.set_dealer(socket, dealer);

def set_starting_stack(socket):
	## ToDo
	global player1
	global player2

def reset_board(socket):
    global board
    board = []
    envoi_cartes.hide_everything(socket)

def set_dealer(socket):
	print("WIP");

def set_blinds(socket):
	print("WIP")

def bet(socket, player, amount, pot_size, bet_type):
	if (bet_type == "call")
		message = "Calls " + amount + "$"
	else if (bet_type == "raise")
		message = "Raises " + amount + "$"
	else if (bet_type == "bet")
		message = "Bets " + amount + "$"
	else if (bet_type == "blind")
		message = "Posts " + amount + "$ blind"
	player["stack"] -= amount
	pot_size[0] += amount
	print("Message still to send")
	# Envoyer taille du pot action et nouveau stack joueur

def give_option(socket, player_number):
	print("WIP")

def exec_action(socket, players, who, action, player_bets, pot):
	give_option(socket, who)
	while (1):
		action = input(players[who]["name"]+ " action")
		if (action == "check")
			print("WIP message")
		else if (action == "call"):
			player_bets[who] = player_bets[(who + 1) % 2]
			print("Display WIP")
		else if (action == "bet"):
			while (1):
				try:
					amount = int(input("How much: "))
					if (amount > players)
						raise CustomErr()
				except ValueError:
					print("Amount invalid")
				except CustomErr:
					print("Amount should be below player stack")
				else:
					break;
			bet(socket, players[who], diff, pot, action)
		else if (action == "raise"):
			while (1):
				try:
					diff = abs(player_bets[0] - player_bets[1])
					amount = int(input("How much: "))
					if (amount + diff > players[who]["stack"])
						raise ValueError("Too much")
				except ValueError as e:
					if (e.message == "Too much")
						print("Error: Value should be below player stack")
					else
						print("Invalid Amount")
				else:
					break;
			bet(socket, players[who], diff, pot, action)
		else if (action == "call")
			diff = abs(player_bets[0] - player_bets[1])
			print("Message WIP")
			bet(socket, players[who], diff, pot, action)
		else:
			print("Invalid action")
			continue
	print("Messages are WIP")

def run_street(players, first_to_act, pot_size, player_bets):
	last_action = ""
	action = ""
	acting = first_to_act
	
	print(player_bets)
	# on stoppe si : 
	# les mises sont égalisées	
	last_action = input("P1 action: ")
	exec_action(last_action)
	action = input("P2 action: ")
	exec_action(action)
	if ((last_action == "check" or last_action == "call") and (action == "check" or action == "call")):
		return (True)
	while (action != "call"):
		action = input("P" + acting + "action: ")
		exec_action(action)
		acting = (acting + 1) % 2

def	pay_winner(socket, players, winner, amount):
	if (winner == -1):
		players[0]["stack"] += amount / 2
		players[1]["stack"] += amount / 2
	else
		players[winner]["stack"] += amount
	# A ajouter message

def run_round(socket):
	global player1
	global player2
	global blinds
	players = [player1, player2]
	pot_size = [0]
	dealer =  int(not player1["is_dealer"])
	action_is_on = dealer
	winner = [-1]

	reset_board()
	bet(socket, players[action_is_on], blinds[0], pot_size, "blind")
	bet(socket, players[action_is_on], blinds[1], pot_size, "blind")
	get_cards(socket)
	if (run_street(socket, players, action_is_on, pot_size, winner, blinds)):
		action_is_on = int(player1["is_dealer"])
		get_flop(socket)
		if (run_street(socket, players, action_is_on, pot_size, winner, [0, 0])):
			get_turn(socket)
			if (run_street(socket, players, action_is_on, winner, [0, 0])):
				get_river(socket)
				run_street(socket, players, action_is_on, winner, [0, 0])
	pay_winner(socket, players, winner[0], pot_size[0])

commands = {"hide": envoi_cartes.hide_everything,
            "get_cards": get_cards,
            "get_flop": get_flop,
            "get_turn": get_turn,
            "get_river": get_river,
            "reset": reset,
			"set_player_names": set_player_names,
			"set_dealer": set_dealer,
			"run_round": run_round,
			"set_blinds": set_blinds
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


# ToDo :	envoi_cartes.set_dealer()
#			set_starting_stack()
#			add_chips()
#			move_chips()
#			run_round()
#			des messages partout
#			OBS joli, ca reste une émission de poker le but..
#			Definir CustomErr