from fastapi import FastAPI
from app.routes import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def home():
    return {"message": "Bienvenue sur l'API FastAPI"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
