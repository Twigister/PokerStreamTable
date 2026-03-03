from fastapi import FastAPI

from fastapi_mqtt import FastMQTT, MQTTConfig
from contextlib import asynccontextmanager

from app.routes import users

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