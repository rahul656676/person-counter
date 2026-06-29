from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from detector import generate_frames

app = FastAPI()

templates = Jinja2Templates(directory="templates")

VIDEO_PATH = "videos/people.mp4"


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.get("/video")
def video_feed():

    return StreamingResponse(
        generate_frames(VIDEO_PATH),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )