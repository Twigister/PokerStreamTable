import envoi_cartes
import probas
import obswebsocket
import keys

import time

p1_cards = ""
p2_cards = ""
board = []

P1_1 = ""
P1_2 = ""
P2_1 = ""
P2_2 = ""

def reset(socket):
    p1_cards = ""
    p2_cards = ""
    board = []

    P1_1 = ""
    P1_2 = ""
    P2_1 = ""
    P2_2 = ""
    envoi_cartes.hide_everything(socket)

def get_cards(socket):
    p1_cards = input()
    tmp = p1_cards.split()
    if (tmp.len() == 2):
        p1_cards = tmp
    print(p1_cards)
    
    p2_cards = input()
    tmp = p2_cards.split()
    if (tmp.len() == 2):
        p2_cards = tmp
    print(p2_cards)
    
    res = probas.get_eq(p1_cards.split() + p2_cards.split(), [])
    print(res)
    P1_1 = p1_cards[0]
    P1_2 = p1_cards[1]
    P2_1 = p2_cards[0]
    P2_2 = p2_cards[1]
    envoi_cartes.change_text(socket, 1, envoi_cartes.fast_type("{0} {1}".format(P1_1, P1_2)), res[0])
    envoi_cartes.change_text(socket, 2, envoi_cartes.fast_type("{0} {1}".format(P2_1, P2_2)), res[1])

def get_flop(socket):
    flop = ["9h", "Th", "2d"]
    board = flop.copy()
    for i in range(len(flop)):
        flop[i] = envoi_cartes.fast_type(flop[i])
    envoi_cartes.set_flop(socket, flop)
    res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], board)
    envoi_cartes.set_eq(socket, 1, res[0])
    envoi_cartes.set_eq(socket, 2, res[1])


def get_turn(socket):
    turn = "Jh"
    board.append(turn)
    turn = envoi_cartes.fast_type(turn)
    envoi_cartes.set_turn(socket, turn)
    res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], board)
    envoi_cartes.set_eq(socket, 1, res[0])
    envoi_cartes.set_eq(socket, 2, res[1])


def get_river(socket):
    river = "Ah"
    board.append(river)
    river = envoi_cartes.fast_type(river)
    envoi_cartes.set_river(socket, river)
    res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], board)
    envoi_cartes.set_eq(socket, 1, res[0])
    envoi_cartes.set_eq(socket, 2, res[1])

def reset_board(socket):
    board = []
    envoi_cartes.hide_everything(socket)

commands = {"hide": envoi_cartes.hide_everything,
            "get_cards": get_cards,
            "get_flop": get_flop,
            "reset": reset}

def run_command(command, socket):
    command = command.split()
    if command[0] in commands:
        commands[command[0]](socket)
    else:
        print("Invalid command\n")

if __name__ == "__main__":
    socket = obswebsocket.obsws(keys.host, keys.port, keys.passw)
    socket.connect()
    while (1):
        command = input("$> ")
        if (command == "exit"):
            break
        run_command(command, socket)
    socket.disconnect()