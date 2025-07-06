from fastapi import FastAPI
from settings import config
from api.enpoints import main_router
import uvicorn


app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host=config.server.host,
        port=config.server.port
    )
