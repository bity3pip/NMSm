from fastapi import FastAPI
from routers import notes, analyse
from database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(notes.router, prefix="/notes", tags=["notes"])
app.include_router(analyse.router, prefix="/analyses" ,tags=["analyses"])
@app.get("/")
def read_root():
    return {"Hello": "World"}
