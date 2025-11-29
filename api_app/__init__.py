from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import db

app = FastAPI(title="All-in-one API Demo")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    db.init_db()


# Import modules to register routes on the `app` instance.
from . import rest  # noqa: E402,F401
from . import soap  # noqa: E402,F401
from . import grpc_sim  # noqa: E402,F401
from . import graphql_api  # noqa: E402,F401
from . import webhooks  # noqa: E402,F401
from . import ws  # noqa: E402,F401
from . import webrtc  # noqa: E402,F401
from . import root  # noqa: E402,F401

__all__ = ["app"]
