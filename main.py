from fastapi import FastAPI, Query, Path
from typing import Optional, List
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
4. 
Query of FastAPI is for extra validation of query parameter, like we can set max_length or min_length of query value,
we can also use regex to match pattern in query parameter.
5.
we can declare function with 'async def' or with normal 'def', FastAPI handle both.
None is used to define it is optional query, we can use Ellipsis(...) with Query to make query parameter required.
6.
Metadata: metadata for query parameter is extra information used by documentation UI or external tool
title: used to add information about parameter.
description: used to describe the use of parameter and other information.
7.
Alias for query parameter: what if we want 'item-query' as query parameter but it is not a valid python variable,
In this case we can declare alias for any variable.
8.
Deprecating: Let suppose if we don't want some query parameter but You have to leave it there a while because 
there are clients using it, but you want the docs to clearly show it as deprecated. \
9. 
we can keep path parameter using is using Path method because python will complain about you can put parameter with  
default value before parameter without any default value, FastAPI will identify these with their name and declaration.
10.
If we really want to keep order of path parameter first with default value and then query parameter, Pass *, as the 
first parameter of the function. 
Python won't do anything with that *, but it will know that all the following parameters should be called as 
keyword arguments (key-value pairs), also known as kwargs. Even if they don't have a default value.
11.
Number validation in path parameter, pass these in Path method:
ge=numeric_value (ge means greater than equal to)
gt=numeric_value (greater than)
le=numeric_value (less than equal to)
lt=numeric_value (less than)
12.
In case of float validation use gt or lt only, In case of float FastAPI will validate any float but 0.0 or 0 is not
valid float.

"""


app = FastAPI()


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]
    description: Optional[str] = None


@app.get('/blog')
def blog_list(limit: int = 10, published: bool = Query(True, alias="published-status"),
              sort: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixed_query$", deprecated=True)):
    if published:
        return {"data": f"{limit} published blogs from db"}
    return {"data": f"{limit} blogs from db, {sort}"}


@app.get('/items/')
async def read_items(name: str = Query("fixed_name", min_length=3),
                     title="Accept name of blog",
                     description="This is query parameter and contain default value, so you may not pass it.",):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if name:
        results.update({"name": name})
    return results


@app.get("/items2/")
async def read_items(q: str = Query(..., min_length=3)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items3/")
async def read_items(data: Optional[List[str]] = Query(None)):
    # URL for this path look likes: http://localhost:8000/items/?data=foo&data=bar
    query_items = {"data": data}
    # Response look likes:
    """{
        "data": [
            "foo",
            "bar"
        ]
        }"""
    return query_items


@app.get("/items4/")
async def read_items(q: List[str] = Query(["foo", "bar"])):
    # List query parameter with default value.
    query_items = {"q": q}
    return query_items


@app.get("/items5/")
async def read_items(q: list = Query([])):
    # we can use list instead of List[str], in this case FastAPI will not check content of list.
    query_items = {"q": q}
    return query_items


@app.post('/blog')
async def create_blog(req: Blog):
    return {'data': f'Blog is created with title {req.title}'}


@app.post('/blog/{user_id}')
async def create_blog(*, user_id: int = Path(..., title="user_id to get all blogs for this user.", ge=0, le=1000),
                      req: Blog, published: Optional[bool] = False):
    return {'data': f'Blog is created with title {req.title} and user is {user_id} with publish status {published}'}


@app.get('/blog/{id}')
def show(id: int = Path(..., title="The user_id for which blog belongs."),
         size: float = Query(..., alias="item-size", gt=0, lt=10.5)):
    return {"data": id, "extra_query_info": size}


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
