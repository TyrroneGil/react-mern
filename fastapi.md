---
marp: true
title: Introduction to FastAPI in Python
paginate: true
---

# Introduction to FastAPI

**FastAPI** is a modern web framework for building APIs with **Python 3.7+**.

It is designed to be:
- Fast
- Easy to use
- Automatic documentation
- Based on Python type hints

---

# Why Use FastAPI?

FastAPI is popular because it provides:

- ⚡ High performance
- 🧠 Easy to learn
- 📄 Automatic API documentation
- 🔒 Data validation
- 🚀 Built on modern Python features

Many developers use FastAPI for **machine learning APIs, web services, and backend systems**.

---

# Installing FastAPI

To install FastAPI, run:

```bash
pip install fastapi
```

You also need an ASGI server like **Uvicorn**:

```bash
pip install uvicorn
```

---

# Basic FastAPI Application

Example of a simple FastAPI program:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

This creates a **basic API endpoint**.

---

# Running the FastAPI Server

Run the server using:

```bash
uvicorn main:app --reload
```

Explanation:

- **main** → filename (`main.py`)
- **app** → FastAPI instance
- **--reload** → automatically reloads when code changes

---

# API Endpoints

FastAPI supports different HTTP methods:

| Method | Description |
|------|-------------|
| GET | Retrieve data |
| POST | Create data |
| PUT | Update data |
| DELETE | Remove data |

Example:

```python
@app.get("/items")
def get_items():
    return {"items": ["item1", "item2"]}
```

---

# Path Parameters

FastAPI allows dynamic values in URLs.

Example:

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

If the user visits:

```
/items/5
```

The API returns:

```
{"item_id": 5}
```

---

# Request Body with Pydantic

FastAPI uses **Pydantic** for data validation.

Example:

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item
```

This ensures the request contains **valid data types**.

---

# Automatic API Documentation

FastAPI automatically creates API documentation.

After running the server, open:

Swagger UI:

```
http://127.0.0.1:8000/docs
```

Alternative Docs:

```
http://127.0.0.1:8000/redoc
```

This allows developers to **test APIs directly in the browser**.

---

# Advantages of FastAPI

✔ Very fast performance  
✔ Easy API development  
✔ Built-in validation  
✔ Automatic documentation  
✔ Ideal for machine learning APIs

---

# Summary

FastAPI is a powerful Python framework used to build modern APIs.

Key features:
- High performance
- Easy to learn
- Automatic documentation
- Strong data validation

It is widely used in **AI systems, backend services, and modern web applications**.

---