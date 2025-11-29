from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect

from . import app
from . import db

# Global memory store
rooms: Dict[str, List[WebSocket]] = {}  # room_name -> list of connections


async def broadcast(room: str, message: str):
    if room not in rooms:
        return
    for connection in list(rooms[room]):
        try:
            await connection.send_text(message)
        except:
            pass


@app.websocket("/ws/chat/{room}/{username}")
async def websocket_chat(ws: WebSocket, room: str, username: str):
    await ws.accept()

    if room not in rooms:
        rooms[room] = []

    rooms[room].append(ws)

    join_msg = f"🔵 {username} joined room: {room}"
    await broadcast(room, join_msg)
    db.save_chat(room, "SYSTEM", join_msg)

    try:
        while True:
            text = await ws.receive_text()
            message = f"{username}: {text}"
            db.save_chat(room, username, text)
            await broadcast(room, message)
    except WebSocketDisconnect:
        rooms[room].remove(ws)
        leave_msg = f"🔴 {username} left room: {room}"
        db.save_chat(room, "SYSTEM", leave_msg)
        await broadcast(room, leave_msg)


@app.get("/chat/{room}")
def get_chat_history(room: str):
    conn = db.get_conn()
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE IF NOT EXISTS chat_history (id INTEGER PRIMARY KEY AUTOINCREMENT, room TEXT, username TEXT, message TEXT)"
    )

    rows = cur.execute(
        "SELECT username, message FROM chat_history WHERE room = ? ORDER BY id",
        (room,),
    ).fetchall()

    conn.close()
    return [{"username": r["username"], "message": r["message"]} for r in rows]
