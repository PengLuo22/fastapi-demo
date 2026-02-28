from fastapi import FastAPI,Path
from pydantic import BaseModel,Field

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World 2026/02/26"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

# path 参数
@app.get("/items/{item_name}")
async def read_item(item_name: str = Path(min_length=2, max_length=10)):
    return {"item_name": item_name}

# query 参数
@app.get("/items/page")
async def read_item(cur_page: int = 1, page_size: int = 10):
    return {"cur_page": cur_page, "page_size": page_size}


# body 参数
class User(BaseModel):
    name: str = Field(min_length=1,max_length=10)
    password: str = Field(min_length=4,max_length=8)

@app.post("/register")
async def regiter(user: User):
    return {"user": user}


