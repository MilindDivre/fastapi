from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def index():
    return "hello world1"

@app.get("/patients")
def index():
    return "lists of patiens"
