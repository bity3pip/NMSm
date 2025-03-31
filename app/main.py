from fastapi import FastAPI
from .database import Base, engine
from .routers import notes, analyse, gemini_end


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(analyse.router, prefix="/analyses" ,tags=["analyses"])
app.include_router(gemini_end.router, prefix="/gemini", tags=["gemini_end"])
@app.get("/")
def read_root():
    return {"Hello": "World"}
