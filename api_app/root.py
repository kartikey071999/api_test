from . import app

#test
@app.get("/")
def root():
    return {
        "message": "All-in-one API demo",
        "endpoints": {
            "REST list tasks": "GET /rest/tasks",
            "REST create task": "POST /rest/tasks",
            "SOAP get task": "POST /soap (XML)",
            "Simulated gRPC add": "POST /grpc/add",
            "GraphQL": "POST /graphql",
            "Webhook receive": "POST /webhooks/receive",
            "Webhook events": "GET /webhooks/events",
            "WebSocket chat": "WS /ws/chat",
            "WebRTC offer": "POST /webrtc/offer",
        },
    }
