from fastapi import Request
from fastapi.responses import PlainTextResponse
import xml.etree.ElementTree as ET

from . import app
from . import db


@app.post("/soap", response_class=PlainTextResponse)
async def soap_endpoint(request: Request):
    body = await request.body()
    try:
        root = ET.fromstring(body.decode("utf-8"))
    except Exception:
        return PlainTextResponse(
            '<Envelope><Body><Error>Invalid XML</Error></Body></Envelope>',
            media_type="text/xml",
            status_code=400,
        )

    task_id = None
    for elem in root.iter():
        if elem.tag.lower().endswith("id"):
            task_id = elem.text
            break

    if not task_id:
        return PlainTextResponse(
            '<Envelope><Body><Error>Missing task id</Error></Body></Envelope>',
            media_type="text/xml",
            status_code=400,
        )

    try:
        task_id_int = int(task_id)
    except ValueError:
        return PlainTextResponse(
            '<Envelope><Body><Error>Invalid task id</Error></Body></Envelope>',
            media_type="text/xml",
            status_code=400,
        )

    conn = db.get_conn()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id, title, status FROM tasks WHERE id = ?",
        (task_id_int,),
    ).fetchone()
    conn.close()

    if not row:
        xml = (
            "<Envelope><Body><GetTaskResponse>"
            "<Found>false</Found>"
            "</GetTaskResponse></Body></Envelope>"
        )
    else:
        xml = (
            "<Envelope><Body><GetTaskResponse>"
            f"<Found>true</Found>"
            f"<Id>{row['id']}</Id>"
            f"<Title>{row['title']}</Title>"
            f"<Status>{row['status']}</Status>"
            "</GetTaskResponse></Body></Envelope>"
        )

    return PlainTextResponse(xml, media_type="text/xml")
