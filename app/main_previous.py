####  https://www.youtube.com/watch?v=0sOvCWFmrtA


from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app  = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:   
    try:
        conn = psycopg2.connect(
            host="localhost",
            database='fastapi',
            user='postgres',
            password='123456', 
            cursor_factory=RealDictCursor
            )
        cursor = conn.cursor()
        print("database connection was successufl!")
        break
    except Exception as error:
        print("Connection to database failed")
        print(error)
        time.sleep(2)
    



my_posts = [
    {'id':1, 'title': 'Top beaches in Florida', 'content': 'check out these awesome beaches', 'published': False, 'rating': 3},
    {'id':2, 'title': 'Top mountains in Florida', 'content': 'check out these awesome mountains', 'published': False, 'rating': 4}
]

def find_post(id):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    post = cursor.fetchone()
    return post
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Welcome to my API world!"}

@app.get("/posts")
async def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"data": post}

@app.get("/posts/{id}")
async def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id=%s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"data": post}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post:Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()

    return {"data": new_post}

@app.post("/createposts2")
async def create_posts2(payload: dict = Body(...)):
    print(payload)
    return {
        "message": "your post was created.",
        "new_post": f" title: {payload['title']} \n content: {payload['content']}"
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"message": "your post was deleted successfully"}

@app.put("/posts/{id}")
async def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated = cursor.fetchone()
    conn.commit()

    if updated == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"data": updated}