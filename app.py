
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from init import SessionLocal, generate_code, encrypt_content, decrypt_content
from model import Note

# Template setup
templates = Jinja2Templates(directory="templates")

# Initialize FastAPI app
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create", response_class=HTMLResponse)
async def create_note(request: Request, content: str = Form(...)):
    if not content:
        raise HTTPException(status_code=400, detail="Content cannot be empty")

    code = generate_code()
    encrypted_content = encrypt_content(content)

    db = SessionLocal()
    db_note = Note(code=code, content=encrypted_content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    db.close()

    return templates.TemplateResponse("note_created.html", {"request": request, "code": code})

@app.get("/retrieve", response_class=HTMLResponse)
async def retrieve(request: Request):
    return templates.TemplateResponse("retrieve.html", {"request": request})

@app.post("/note", response_class=HTMLResponse)
async def view_note(request: Request, code: str = Form(...)):
    db = SessionLocal()
    db_note = db.query(Note).filter(Note.code == code).first()

    if db_note is None:
        db.close()
        raise HTTPException(status_code=404, detail="Invalid code or note not found")

    decrypted_content = decrypt_content(db_note.content)
    if decrypted_content is None:
        db.close()
        raise HTTPException(status_code=500, detail="Failed to decrypt the note")

    # Delete the note after viewing
    db.delete(db_note)
    db.commit()
    db.close()

    return templates.TemplateResponse("view_note.html", {"request": request, "note": decrypted_content})

@app.exception_handler(404)
async def not_found_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "message": "Page not found"}, status_code=404)

@app.exception_handler(500)
async def internal_error_exception(request: Request, exc: HTTPException):
    return templates.TemplateResponse("error.html", {"request": request, "message": "Internal Server Error"}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
