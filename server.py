"""
ILLI Backend Server: FastAPI for local API, WebSockets, and model management.
"""
from fastapi import FastAPI, WebSocket
import uvicorn

app = FastAPI(title="ILLI Local Backend")

@app.get("/status")
async def get_status():
    return {"status": "ILLI Backend Operational"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")