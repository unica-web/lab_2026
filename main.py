from fastapi import FastAPI


app = FastAPI()


@app.get("/")
def hello_world(
    q: str,
    sort: bool = False
) -> dict[str, str | bool]:
    return {"q": q, "sort": sort}


@app.get("/home")
def homepage():
    return "This is the homepage"


@app.get("/{username}")
def username_webpage(
    username: str
):
    return f"This is the webpage of user {username}."


@app.get("/{username}/orders/{order_id}")
def orders_webpage(
    username: str,
    q: str,
    order_id: int,
    sort: bool = False
):
    return f"Order {order_id} for user {username}. Q: {q}. Sorted: {sort}."
