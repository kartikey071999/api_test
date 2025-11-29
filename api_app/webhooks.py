from . import app
from . import db
from .models import WebhookPayload


@app.post("/webhooks/receive")
def webhook_receive(body: WebhookPayload):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO webhook_events (source, payload) VALUES (?, ?)",
        (body.source, str(body.payload)),
    )
    conn.commit()
    conn.close()
    return {"stored": True}


@app.get("/webhooks/events")
def webhook_events():
    conn = db.get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, source, payload FROM webhook_events ORDER BY id").fetchall()
    conn.close()
    return [{"id": r["id"], "source": r["source"], "payload": r["payload"]} for r in rows]
