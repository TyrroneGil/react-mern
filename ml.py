from fastapi import FastAPI

app = FastAPI()

@app.get('/getDetails')
def details():
    
    return {"message":"Return"}