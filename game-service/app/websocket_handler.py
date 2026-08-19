from fastapi import WebSocket, Depends
from fastapi.encoders import jsonable_encoder
import json
from app import crud
from app.db import get_db
from sqlalchemy.orm import Session

from app.schemas import UserOut

async def init_handler(websocket: WebSocket, json_data, db: Session):
    try:
      users = crud.get_table_state(db, table_id=json_data["content"]["table_id"]) 
      res = [None] * 10
      for u in users:
          res[u.seat_number - 1] = UserOut.model_validate(u)
    except KeyError:
      await websocket.send_text("Error while fetching table number")
    else:
      await websocket.send_text(json.dumps(jsonable_encoder({"type": "init", "content": res})))

async def websocket_handler(websocket: WebSocket, db: Session):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        try:
            json_data = json.loads(data)
            json_data["type"]
        except json.JSONDecodeError:
            await websocket.send_text("Invalid JSON received")
            continue
        except KeyError:
            await websocket.send_text("Missing 'type' field in JSON")
            continue

        match json_data["type"]:
            case "init":
              await init_handler(websocket, json_data, db)
              pass
            case "seat":
                await websocket.send_text(f"Seat message received: {json_data}, WIP")
                pass
            case _:
                await websocket.send_text(f"Unknown message type: {json_data['type']}")
                pass
