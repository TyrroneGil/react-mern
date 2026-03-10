from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import os
from compare import HeartSoundClassifier

app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

classifier = HeartSoundClassifier()
UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/uploadImage")
async def uploadImage(image: UploadFile = File(...)):
    
    file_path = os.path.join(UPLOAD_FOLDER, image.filename)

    with open(file_path, "wb") as f:
        contents = await image.read()
        f.write(contents)

    prediction,accuracy=classifier.predict_image(file_path)

    return {
        "prediction":prediction,
        "accuracy":accuracy
    }