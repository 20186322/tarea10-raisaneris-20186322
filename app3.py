from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
from uuid import uuid4 as uuid
import uvicorn

app = FastAPI()

posts = []

class Post(BaseModel):
    Codigo: str
    Tipo: str
    Nombre: str
    Precio: str
    Cantidad: str
    Comentario: str

@app.get('/')
def read_root():
    return {"Bienvenidos": "Bienvenidos a mi API"}

@app.get('/posts')
def get_posts():
    return posts

@app.post('/posts')
def save_post(post: Post):
    post.id = str(uuid())
    posts.append(post.dict())
    return posts[-1]

@app.get('/posts/{post_id}')
def get_post(post_id: str):
    for post in posts:
        if post["id"] == post_id:
            return post
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete('/posts/{post_id}')
def delete_post(post_id: str):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts.pop(index)
            return {"message": "Factura ha sido eliminada exitosamente"}
    raise HTTPException(status_code=404, detail="Item not found")

@app.put('/posts/{post_id}')
def update_post(post_id: str, updatedPost: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["Codigo"]= updatedPost.dict()["Codigo"]
            posts[index]["Tipo"]= updatedPost.dict()["Tipo"]
            posts[index]["Nombre"]= updatedPost.dict()["Nombre"]
            posts[index]["Precio"]= updatedPost.dict()["Precio"]
            posts[index]["Cantidad"]= updatedPost.dict()["Cantidad"]
            posts[index]["Comentario"]= updatedPost.dict()["Comentario"]
            return {"message": "La factura se ha actualizado exitosamente"}
    raise HTTPException(status_code=404, detail="Item not found")