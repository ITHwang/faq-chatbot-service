from enum import Enum
from typing import Annotated

from fastapi import Body, FastAPI, File, Form, Query, Path, Response, UploadFile, status
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, EmailStr, Field, HttpUrl


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


##########################################
# Path Parameters
##########################################


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


# additional validation of path parameter
@app.get("/items3/{item_id}")
async def read_item3(
    item_id: Annotated[int, Path(title="The ID of the item to get", gt=0, le=1000)],
    q: str,
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


##########################################
# Query Parameters
##########################################


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items")
async def read_item2(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# additional validation of query string
@app.get("/items2/")
async def read_items2(q: Annotated[str | None, Query(min_length=3, max_length=50)] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


##########################################
# Request Body
##########################################


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(default=None, title="The description of the item", max_length=300)
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None
    tags: set[str] = set()
    images: list[Image] | None = None


# deeply nested models
class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item]


class User(BaseModel):
    username: str
    full_name: str | None = None


@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    """
    If the parameter is also declared in the path, it will be used as a path parameter.
    If the parameter is of a singular type (like int, float, str, bool, etc) it will be interpreted as a query parameter.
    If the parameter is declared to be of the type of a Pydantic model, it will be interpreted as a request body.
    """
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# you can instruct FastAPI to treat it as another body key using Body:
@app.put("/items2/{item_id}")
async def update_item2(item_id: int, item: Item, user: User, importance: Annotated[int, Body()]):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.post("/images/multiple/")
async def create_multiple_images(images: list[Image]):
    return images


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


# if you want to receive keys that you don't already know,
@app.post("/index-weights/")
async def create_index_weights(weights: dict[int, float]):
    # Keep in mind that JSON only supports str as keys.
    # But Pydantic has automatic data conversion.
    return weights


# it is required to send a username and password as form fields.
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


# It uses a "spooled" file which is a file stored in memory up to a maximum size limit, and after passing this limit it will be stored in disk.
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


##########################################
# Response Model
##########################################

# It will limit and filter the output data to what is defined in the return type.
# This is particularly important for security, we'll see more of that below.


@app.post("/items2", response_model=Item)
async def create_item2(item: Item) -> Item:
    return item


@app.get("/items/", response_model=list[Item])
async def read_items() -> list[Item]:
    return [
        Item(name="Portal Gun", price=42.0),
        Item(name="Plumbus", price=32.0),
    ]


class BaseUser(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(BaseUser):
    password: str


# filtering out all the data that is not declared in the output model
@app.post("/user/")
async def create_user(user: UserIn) -> BaseUser:
    return user


# return something that is not a valid Pydantic field
@app.get("/portal")
async def get_portal(teleport: bool = False) -> Response:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=zxzxzx")
    return JSONResponse(content={"message": "Here's your interdimensional portal."})
