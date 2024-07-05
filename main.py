import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.api import router

app = FastAPI()
app.include_router(router, prefix="/api", tags=[""])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
    allow_credentials=True,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=10086, reload=True)
