####  https://www.youtube.com/watch?v=0sOvCWFmrtA


from typing import Optional, List
from fastapi import Depends, FastAPI, Response, status, HTTPException
from fastapi.params import Body


from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models, schemes, utils
from .database import SessionLocal, engine, get_db



models.Base.metadata.create_all(bind=engine)

app  = FastAPI()


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
        print("database connection was successful!")
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

@app.get("/testSQL", response_model=List[schemes.Post])
def get_test_SQL(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    print(posts)
    return posts

@app.get("/posts", response_model=List[schemes.Post])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@app.get("/posts/latest", response_model=schemes.Post)
async def get_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at)
    print(post)
    return post.first()

@app.get("/posts/{id}", response_model=schemes.Post)
async def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemes.Post)
async def create_posts(post:schemes.PostCreate, db: Session = Depends(get_db)):
    ##### new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_post = models.Post(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    post.delete(synchronize_session=False)
    db.commit()

    return {"message": "your post was deleted successfully"}

@app.put("/posts/{id}", response_model=schemes.Post)
async def update_post(id: int, post: schemes.PostCreate, db: Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    old_value = post_query.first()

    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()

    if old_value == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post_query.first()



@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemes.UserOut)
async def create_user(user:schemes.UserCreate, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    ##### new_post = models.Post(title=post.title, content=post.content, published=post.published)
    new_user = models.User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get('/users/{id}', response_model=schemes.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} does not exist")
    
    return user