from PyQt6.QtWidgets import QApplication
import sys
import keys
from utils import *
import obsws_python as obs

from qt.Window import Window

import globalv
import communication.requests

# MQTT doit pouvoir communiquer avec le client OBS et faire les changements adéquats sur l'application [TBR]
if __name__ == "__main__":
	try:
		app = QApplication(sys.argv)
		cl = obs.ReqClient(host=keys.host, port=keys.port, password=keys.passw, timeout=3)
		globalv.cl = cl
		window = Window()
		window.show()
		mqtt = communication.requests.init(window)
		mqtt.loop_start()

		ret = app.exec()
		cl.disconnect()
		sys.exit(ret)
	except Exception as e:
		print(e)
		print("Uh Oh")