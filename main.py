from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import Field, BaseModel


class Product(BaseModel):
    name: Annotated[str, Field(min_length=3, max_length=30)]
    price: Annotated[float, Field(gt=0)]
    location: Annotated[str, Field(min_length=3)]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


product_list = [
    {"name": "notebook DELL", "price": 2999.99, "location": "Cagliari"},
    {"name": "smartphone Xiaomi", "price": 999.99, "location": "Napoli"},
    {"name": "tablet Samsung", "price": 1499.99, "location": "Firenze"},
    {"name": "headphones JBL", "price": 499.99, "location": "Torino"},
    {"name": "watch Samsung", "price": 1999.99, "location": "Milano"}
]


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Renders the home page.
    """
    return templates.TemplateResponse(
        request=request,
        name="home.html",
        context={"text": "Welcome to the store"}
    )


@app.get("/products", response_class=HTMLResponse)
def products(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="products.html",
        context={"product_list": product_list}
    )


@app.get("/product_form", response_class=HTMLResponse)
def add_product(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="product_form.html"
    )


@app.post("/insert_product")
def insert_product(
    product: Annotated[Product, Form()]
):
    product_list.append(product.model_dump())
    return "Product added successfully"


@app.post("/insert_product_json")
def insert_product_json(
    product: Product
):
    product_list.append(product.model_dump())
    return "Product added successfully"
