import paho.mqtt.client as mqtt
from communication.deck_decode import deck
from qt.Window import Window

global table

def on_connect(client, userdata, flags, rc):
	print(f"Connected with the mqtt broker with result code {rc}")
	client.subscribe("nfc/tafreader")

def on_message(client, userdata, msg):
	str = msg.payload.decode()
	print(f"MQTT feed update: {str}")
	try:
		pno = int(int(str[0]) / 2)
		card = deck[str[1:]]
		if pno < 2:
			pcar = int(str[0]) % 2
			window.setCard(pno, pcar, card)
		elif pno >= 2:
			pno = 3
			pcar = int(str[0]) - 4
			print(f"Putting card {card} to board, no {pcar}")
			window.setBoardCard(pcar, card)
	except:
		print("Error: Invalid mqtt message")

def init(tabol: Window):
	client = mqtt.Client()
	global window
	window = tabol
	client.on_connect = on_connect
	client.on_message = on_message

	client.connect("localhost", 1883, 60)  # Connect to the local broker on port 1883
	return client
