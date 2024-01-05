import envoi_cartes
import probas
import obswebsocket
import keys

import time

socket = obswebsocket.obsws(keys.host, keys.port, keys.passw)
socket.connect()

envoi_cartes.hide_everything(socket)

P1_1 = "As"
P1_2 = "Ad"
P2_1 = "7h"
P2_2 = "8h"

res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], [])

envoi_cartes.change_text(socket, 1, envoi_cartes.fast_type("{0} {1}".format(P1_1, P1_2)), res[0])
envoi_cartes.change_text(socket, 2, envoi_cartes.fast_type("{0} {1}".format(P2_1, P2_2)), res[1])

print(res)

flop = ["9h", "Th", "2d"]
turn = "Jh"
river = "Ah"
board = flop.copy()

for i in range(len(flop)):
    flop[i] = envoi_cartes.fast_type(flop[i])

time.sleep(10)

envoi_cartes.set_flop(socket, flop)
res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], board)
envoi_cartes.set_eq(socket, 1, res[0])
envoi_cartes.set_eq(socket, 2, res[1])

time.sleep(10)

board.append(turn)
turn = envoi_cartes.fast_type(turn)
envoi_cartes.set_turn(socket, turn)
res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], board)
envoi_cartes.set_eq(socket, 1, res[0])
envoi_cartes.set_eq(socket, 2, res[1])

time.sleep(10)

board.append(river)
river = envoi_cartes.fast_type(river)
envoi_cartes.set_river(socket, river)
res = probas.get_eq([P1_1, P1_2, P2_1, P2_2], board)
envoi_cartes.set_eq(socket, 1, res[0])
envoi_cartes.set_eq(socket, 2, res[1])

socket.disconnect()
