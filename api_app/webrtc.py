from . import app
from .models import WebRTCOffer, WebRTCAnswer


@app.post("/webrtc/offer", response_model=WebRTCAnswer)
def fake_webrtc_offer(body: WebRTCOffer):
    fake_answer_sdp = "v=0\r\no=- 0 0 IN IP4 127.0.0.1\r\ns=FakeAnswer\r\n"
    return WebRTCAnswer(
        sdp=fake_answer_sdp,
        type="answer",
        note="Fake WebRTC answer – signaling only, no real media.",
    )
