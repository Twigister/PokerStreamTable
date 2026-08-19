from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from fastapi_mqtt import FastMQTT, MQTTConfig
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users

from app.websocket_handler import *

app = FastAPI()

MQTT_CONTAINER = "mosquitto"
MQTT_PORT = 1883
mqtt_running = False

mqtt_config = MQTTConfig(
  host=MQTT_CONTAINER,
  port=MQTT_PORT,
  keepalive=60
)

mqttc = FastMQTT(config=mqtt_config)

@asynccontextmanager
async def _lifespan(_app: FastAPI):
  await mqttc.mqtt_startup()
  yield

app = FastAPI(lifespan=_lifespan)

@mqttc.on_connect()
def handle_connect(client, flags, rc, properties):
  print("Service sucessfully connected to MQTT")
  global mqtt_running; mqtt_running = True
  mqttc.client.subscribe("+/controllers/#")

@mqttc.on_message()
async def handle_message(client, topic, payload, qos, properties):
  contents = payload.decode()
  print(f"Putting to: {topic}: {contents}")


@mqttc.on_disconnect()
def handle_disconnect(client, packet, exc=None):
  print("Disconnected from MQTT")
  global mqtt_running; mqtt_running = False

# FastAPI routes
@app.get("/status")
def status():
  return ({"status" : "Running"} if mqtt_running else {"status": "Error with MQTT"})

app.include_router(users.router)
app.add_middleware(CORSMiddleware,
                    allow_origins=["*"],
                    allow_credentials=True,
                    allow_methods=["*"],
                    allow_headers=["*"])

@app.get("/websocket_interface")
async def get_websocket_interface():
  html = """
  <!DOCTYPE html>
  <html>
      <head>
          <title>Chat</title>
      </head>
      <body>
          <h1>WebSocket Chat</h1>
          <form action="" onsubmit="sendMessage(event)">
              <input type="text" id="messageText" autocomplete="off"/>
              <button>Send</button>
          </form>
          <ul id='messages'>
          </ul>
          <script>
              var ws = new WebSocket("ws://localhost:8000/ws");
              ws.onmessage = function(event) {
                  var messages = document.getElementById('messages')
                  var message = document.createElement('li')
                  var content = document.createTextNode(event.data)
                  message.appendChild(content)
                  messages.appendChild(message)
              };
              function sendMessage(event) {
                  var input = document.getElementById("messageText")
                  ws.send(input.value)
                  input.value = ''
                  event.preventDefault()
              }
          </script>
      </body>
  </html>
  """
  return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
  await websocket_handler(websocket, db)