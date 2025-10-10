from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQTTConfig

from contextlib import asynccontextmanager

from pymongo import MongoClient

# MongoDB
MONGO_CONTAINER="mongodb"
MONGO_PORT=27017
MONGO_USER="admin"
MONGO_PASS="rootpass"
MONGO_DB="poker_stream_table"
mongo_running = True

mongo_uri=f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_CONTAINER}:{MONGO_PORT}/{MONGO_DB}?authSource=admin"
mongo_client=MongoClient(mongo_uri)
mongo_db=mongo_client[MONGO_DB]

# MQTT
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
    await mqttc.mqtt_shutdown()

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
  dest = topic.split("/")
  table=mongo_db["cards"]
  dict = {
    "table_id": dest[0],
    "seat_no": dest[2],
    "cards": contents
  }
  t_id = table.update_one(
    {"_id": topic},
    {"$set": dict},
    upsert=True
  )
  print(f"Successfully inserted {t_id}")

@mqttc.on_disconnect()
def handle_disconnect(client, packet, exc=None):
  print("Disconnected from MQTT")
  global mqtt_running; mqtt_running = False

# FastAPI routes
@app.get("/status")
def status():
  if mqtt_running and mongo_running:
    return {
      "status" : "Running"
    }
  else:
    return {
      "status" : f"Error with {'MQTT' if not mqtt_running else 'MongoDB'}"
    }
