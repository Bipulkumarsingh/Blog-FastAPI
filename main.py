from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

"""
NOTE:
1.
you can use same name for path operation function, like def index() for path='/' and def index() for path='/home/'
FastAPI cares about path not the function name.
2.
path arrangements matter in FastAPI
like if you create path='/blog/{id}' and second one is path='/blog/unpublished'
then second path will be unreachable because first will manage request, considering 'unpublished' as id.
Always keep static routing before dynamic one if they look alike or behave like same.
3.
FastAPI easily identify path parameter and query parameter,
if variable is present int path then in function it is consider as path parameter and query parameter may be optional
one only need to define in function.
"""


app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    description: Optional[str] = None


@app.get('/blog')
def blog_list(limit: int = 10, published: bool = True, sort: Optional[str] = None):
    if published:
        return {"data": f"{limit} published blogs from db"}
    return {"data": f"{limit} blogs from db, {sort}"}


@app.post('/blog')
def create_blog(req: Blog):
    return {'data': f'Blog is created with title {req.title}'}


@app.post('/blog/{user_id}')
def create_blog(user_id: int, req: Blog, published: Optional[bool] = False):
    return {'data': f'Blog is created with title {req.title} and user is {user_id} with publish status {published}'}


@app.get('/blog/{id}')
def show(id: int):
    # Fetch blog with id = id
    return {"data": id}


@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished blogs'}


@app.get('/blog/{id}/comments')
def comments(id: int, limit: int = 10):
    # Fetch comment of blog with id = id
    return {'data': {'comments': id, "limit": limit}}


@app.get('/blog/{id}/comments/{user_id}')
def comments(id: int, user_id: int, limit: int = 10):
    # Fetch comment of blog with id = id
    return {'data': {'comments': id, "user": user_id, "limit": limit}}
