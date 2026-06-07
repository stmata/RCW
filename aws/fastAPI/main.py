from fastapi import FastAPI, HTTPException
from mangum import Mangum
import logging
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

logging.basicConfig(level=logging.INFO)

handler = Mangum(app)

@app.get("/")
async def hello():
    try:
        logging.info("hello endpoint accessed")
        return {"message": "hello from server IA1"}
    except Exception as e:
        logging.error(f"Error in hello endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/test")
async def hello_test():
    try:
        logging.info("hello endpoint accessed")
        return {"message": "hello from server Test"}
    except Exception as e:
        logging.error(f"Error in hello endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
