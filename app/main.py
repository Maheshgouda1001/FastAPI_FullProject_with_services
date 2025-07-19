from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.router import authenticate, plan
import json
from datetime import datetime
from app.db.database import Base, engine
from app.middleware.auth_middleware import JWTAuthMiddleware
from app.services.connection_manager import manager

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(JWTAuthMiddleware)

app.include_router(authenticate.router, prefix="/authenticate", tags=["Authentication"])
app.include_router(plan.router, prefix="/plan", tags=["Planning Page"])

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            print(f"Message from {client_id}: {message}")
            response = {**message, "status": "received", "timestamp": datetime.now().isoformat(), "client_id": client_id}
            if message.get("type") == "broadcast":
                await manager.broadcast(json.dumps(response))
            else:
                await manager.send_message(websocket, json.dumps(response))
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except json.JSONDecodeError:
        await manager.send_message(websocket, json.dumps({"error": "Invalid JSON format", "timestamp": datetime.now().isoformat()}))
    except Exception as e:
        print(f"Error: {e}")
        await manager.disconnect(websocket)
