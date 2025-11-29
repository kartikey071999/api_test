from typing import List
from . import db
from .models import Task, TaskCreate
from . import app


@app.get("/rest/tasks", response_model=List[Task])
def list_tasks():
    conn = db.get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, title, status FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [Task(id=r["id"], title=r["title"], status=r["status"]) for r in rows]


@app.post("/rest/tasks", response_model=Task)
def create_task(task: TaskCreate):
    conn = db.get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        (task.title, task.status),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return Task(id=new_id, title=task.title, status=task.status)


@app.get("/rest/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    conn = db.get_conn()
    cur = conn.cursor()
    row = cur.execute(
        "SELECT id, title, status FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    conn.close()
    if not row:
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=404, content={"detail": "Task not found"})
    return Task(id=row["id"], title=row["title"], status=row["status"])
