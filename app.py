import os, json
import chess.pgn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import logic

app = FastAPI()
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="pages")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("page.html", {"request": request})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    # open file and parse the moves, store in json for later
    pgn_path = os.path.join("uploads", file.filename)
    with open(pgn_path, "wb") as f:
        f.write(await file.read())

    with open(pgn_path) as f:
        game = chess.pgn.read_game(f)

    if not game:
        return {"error": "Invalid PGN file"}

    
    # run algorithm, and then send returned results
    similar_pgn_file = logic.find_game(pgn_path)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "message": "Found similar game!",
            "pgn_url": f"/{similar_pgn_file}"  # file
        }
    )



