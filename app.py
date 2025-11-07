import os, json, uuid
import chess.pgn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
from fastapi.responses import RedirectResponse

from data_loader import load_pgn_database
from rabin_karp import find_most_similar_game

database_games = load_pgn_database("lichess_db_standard_rated_2013-01.pgn.zst", max_games=1000)


app = FastAPI()
os.makedirs("uploads", exist_ok=True)
os.makedirs("sessions", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/img", StaticFiles(directory="img"), name="img")
templates = Jinja2Templates(directory="pages")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("page.html", {"request": request})

@app.post("/upload")
async def upload_file(request: Request, file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)
    session_id = str(uuid.uuid4())
    pgn_filename = f"{session_id}_{file.filename}"
    pgn_path = os.path.join("uploads", file.filename)
    with open(pgn_path, "wb") as f:
        f.write(await file.read())

    with open(pgn_path, encoding="utf-8", errors="ignore") as f:
        game = chess.pgn.read_game(f)

    if not game:
        return {"error": "Invalid PGN file"}
    
    session_data = {
        "session_id": session_id,
        "pgn_path": pgn_path,
        "options": {}  
    }

    with open(f"sessions/{session_id}.json", "w") as session_file:
        json.dump(session_data, session_file, indent=4)

    return RedirectResponse(
        url=f"/options?session_id={session_id}",  
        status_code=303
    )


@app.get("/options", response_class=HTMLResponse)
async def options(request: Request, session_id: str):
    return templates.TemplateResponse(
        "options.html",
        {"request": request, "session_id": session_id}
    )

@app.post("/compare")
async def compare(
    request: Request,
    session_id: str = Form(...),
    compare_type: str = Form(...),
    winner: str = Form(...),
    search_method: str = Form(...)
):
    session_path = f"sessions/{session_id}.json"
    if not os.path.exists(session_path):
        return {"error": "Session not found"}

    with open(session_path, "r") as f:
        session_data = json.load(f)

    with open(session_data["pgn_path"], "r", encoding="utf-8", errors="ignore") as f:
        input_game = f.read()

    similar_game, score = find_most_similar_game(input_game, database_games, mode="moves")

    similar_game_pgn = f"uploads/{session_id}_similar.pgn"
    with open(similar_game_pgn, "w", encoding="utf-8") as f:
        f.write(similar_game)
    session_data["similar_game_pgn"] = similar_game_pgn

    with open(session_path, "w") as f:
        json.dump(session_data, f, indent=4)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "compare_type": compare_type,
            "winner": winner,
            "search_method": search_method,
            "pgn_url": session_data["similar_game_pgn"],
            "pgn_content": similar_game,
            "similarity_score": score,
            "message": "Options saved successfully!"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

