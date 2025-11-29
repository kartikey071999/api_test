import strawberry
from strawberry.fastapi import GraphQLRouter

from . import app
from . import db


@strawberry.type
class TaskType:
    id: int
    title: str
    status: str


def fetch_tasks_from_db() -> list[TaskType]:
    conn = db.get_conn()
    cur = conn.cursor()
    rows = cur.execute("SELECT id, title, status FROM tasks ORDER BY id").fetchall()
    conn.close()
    return [TaskType(id=r["id"], title=r["title"], status=r["status"]) for r in rows]


@strawberry.type
class Query:
    @strawberry.field
    def tasks(self) -> list[TaskType]:
        return fetch_tasks_from_db()


schema = strawberry.Schema(Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
