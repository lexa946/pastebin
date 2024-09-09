from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from routers import main, front


app = FastAPI()

app.include_router(main.router)
app.include_router(front.router)

app.mount('/static/pastebeen', StaticFiles(directory="pastebeen/static"), 'pastebeen_static')


