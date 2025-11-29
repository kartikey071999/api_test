from . import app
from .models import AddRequest, AddResponse


@app.post("/grpc/add", response_model=AddResponse)
def fake_grpc_add(body: AddRequest):
    res = body.a + body.b
    return AddResponse(
        result=res,
        note="This simulates a gRPC method (Add) using normal HTTP+JSON.",
    )
