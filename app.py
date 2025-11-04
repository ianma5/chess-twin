import os, json, uuid
import chess.pgn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Form
import logic

app = FastAPI()
os.makedirs("uploads", exist_ok=True)
os.makedirs("sessions", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
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

    from fastapi.responses import RedirectResponse
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

    session_data["options"] = {
        "compare_type": compare_type,
        "winner": winner,
        "search_method": search_method
    }
    
    with open(session_path, "w") as f:
        json.dump(session_data, f, indent=4)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "compare_type": compare_type,
            "winner": winner,
            "search_method": search_method,
            "pgn_url": session_data["pgn_path"],
            "message": "Options saved successfully!"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

