from app import app
from db import migrate
import uvicorn


if __name__ == "__main__":
    migrate()
    uvicorn.run(app,host="localhost",port=8080)


