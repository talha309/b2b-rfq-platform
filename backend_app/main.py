from fastapi import FastAPI
from routes import authentication_routes
from database.data_base import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="B2B RFQ Platform API")

app.include_router(authentication_routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to B2B RFQ Platform!"}
