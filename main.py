from typing import Optional, List, Set
from enum import Enum

from fastapi import FastAPI, Query, Path, Body, Form, UploadFile, File
from pydantic import BaseModel, HttpUrl

app = FastAPI()

fake_items_db = [
    {"item_name": "Foo"}, 
    {"item_name": "Bar"}, 
    {"item_name": "Baz"}
  ]


class Image(BaseModel):
  url: HttpUrl
  name: str
  # url: str


class Item(BaseModel):
  name: str
  price: float
  is_offer: Optional[bool] = None


class ModelName(str, Enum):
  alexnet = "alexnet"
  resnet = "resnet"
  lenet = "lenet"


class Product(BaseModel):
  name: str
  description: Optional[str] = None
  price: float
  tax: Optional[float] = None
  tags: Set[str] = []
  images: Optional[List[Image]] = None
  # image: Optional[Image] = None
  # tags: List[str] = []
  # tags: list = []


class User(BaseModel):
  username: str
  full_name: Optional[str] = None


class Offer(BaseModel):
  name: str
  description: Optional[str] = None
  price: float
  items: List[Product]

@app.get("/")
async def read_root():
  return {"Hello": "World"}


# http://127.0.0.1:8000/items/5?q=somequery
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
  return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
  return {"item_name": item.name, "item_id": item_id}


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
  if model_name == ModelName.alexnet:
    return {"model_name": model_name, "message": "Deep Learning FTW!"}

  if model_name.value == "lenet":
    return {"model_name": model_name, "message": "LeCNN all the images"}

  return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
  return {"file_path": file_path}


# http://127.0.0.1:8000/items/?skip=0&limit=10
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
  return fake_items_db[skip : skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None):
  if q:
    return {"item_id": item_id, "q": q}
  return {"item_id": item_id}


# http://127.0.0.1:8000/items/foo?short=1
# http://127.0.0.1:8000/items/foo?short=true
# http://127.0.0.1:8000/items/foo?short=on
# http://127.0.0.1:8000/items/foo?short=yes
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
  item = {"item_id": item_id}
  if q:
    item.update({"q": q})
  if not short:
    item.update(
      {"description": "This is an amazing item that has a long description"}
    )
  return item


# http://127.0.0.1:8000/users/1/items/1
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
  ):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
      item.update({"q": q})
    if not short:
      item.update(
        {"description": "This is an amazing item that has a long description"}
      )
    return item


# http://127.0.0.1:8000/items/foo-item
# http://127.0.0.1:8000/items/foo-item?needy=sooooneedy
@app.get("/items/{item_id}")
async def read_user_item(item_id: str, needy: str):
  item = {"item_id": item_id, "needy": needy}
  return item


@app.get("/items/{item_id}")
async def read_user_item(
    item_id: str, needy: str, skip: int = 0, limit: Optional[int] = None
  ):
  item = {"item_id": item_id, "needy": needy, "skip": skip, "limit": limit}
  return item


# {
#   "name": "Foo",
#   "description": "An optional description",
#   "price": 45.2,
#   "tax": 3.5
# }
# POST http://127.0.0.1:8000/items/
@app.post("/items/")
async def create_item(item: Product):
  return item


@app.post("/items/")
async def create_item(item: Product):
  item_dict = item.dict()
  if item.tax:
    price_with_tax = item.price + item.tax
    item_dict.update({"price_with_tax": price_with_tax})
  return item_dict


# put http://127.0.0.1:8000/items/1
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Product):
  return {"item_id": item_id, **item.dict()}


@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Product, q: Optional[str] = None):
  result = {"item_id": item_id, **item.dict()}
  if q:
    result.update({"q": q})
  return result


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, max_length=50)):
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
    results.update({"q": q})
  return results


@app.get("/items/")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=50)):
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
    results.update({"q": q})
  return results


@app.get("/items/")
async def read_items(q: str = Query("fixedquery", min_length=3)):
  results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
  if q:
    results.update({"q": q})
  return results


@app.get("/items/")
async def read_items(q: Optional[List[str]] = Query(None)):
  query_items = {"q": q}
  return query_items


@app.get("/items/")
async def read_items(q: List[str] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items


@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int = Path(..., title="The ID of the item to get", ge=0, le=1000),
    q: Optional[str] = None,
    item: Optional[Item] = None,
  ):
  results = {"item_id": item_id}
  if q:
    results.update({"q": q})
  if item:
    results.update({"item": item})
  return results


# {
#   "item": {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
#   },
#   "user": {
#     "username": "dave",
#     "full_name": "Dave Grohl"
#   }
# }
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Product, user: User):
  results = {"item_id": item_id, "item": item, "user": user}
  return results


# {
#   "item": {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
#   },
#   "user": {
#     "username": "dave",
#     "full_name": "Dave Grohl"
#   },
#   "importance": 5
# }
# @app.put("/items/{item_id}")
# async def update_item(
#     item_id: int, item: Product, user: User, importance: int = Body(...)
#   ):
#   results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
#   return results


# {
#   "item": {
#     "name": "Foo",
#     "description": "The pretender",
#     "price": 42.0,
#     "tax": 3.2
#   }
# }
# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item = Body(..., embed=True)):
#   results = {"item_id": item_id, "item": item}
#   return results


# {
#   "name": "Foo",
#   "description": "The pretender",
#   "price": 42.0,
#   "tax": 3.2,
#   "tags": ["rock", "metal", "bar"],
#   "image": {
#     "url": "http://example.com/baz.jpg",
#     "name": "The Foo live"
#   }
# }

# {
#   "name": "Foo",
#   "description": "The pretender",
#   "price": 42.0,
#   "tax": 3.2,
#   "tags": [
#     "rock",
#     "metal",
#     "bar"
#   ],
#   "images": [
#     {
#       "url": "http://example.com/baz.jpg",
#       "name": "The Foo live"
#     },
#     {
#       "url": "http://example.com/dave.jpg",
#       "name": "The Baz"
#     }
#   ]
# }
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Product):
  results = {"item_id": item_id, "item": item}
  return results


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
  return images


@app.post("/offers/")
async def create_offer(offer: Offer):
  return offer


@app.post("/login/")
async def login(username: str = Form(...), password: str = Form(...)):
  return {"username": username}


@app.post("/files/")
async def create_file(file: bytes = File(...)):
  return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
  return {"filename": file.filename}


# @app.post("/files/")
# async def create_file(
#     file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)
#   ):
#   return {
#     "file_size": len(file),
#     "token": token,
#     "fileb_content_type": fileb.content_type,
#   }


