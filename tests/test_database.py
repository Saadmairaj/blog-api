import os
import pytest
import requests
from api.database import Blog, CachedSession, Session


def test_env_variable():
    os.environ["BLOG_POST_ROUTE"] = "https://www.google.co.in"
    os.environ["CACHING"] = "true"
    blog = Blog()

    assert blog._route == "https://www.google.co.in"
    assert isinstance(blog._sess, CachedSession)

    del blog

    os.environ["CACHING"] = "false"
    blog = Blog()

    assert isinstance(blog._sess, Session)

    del blog


def test_blog_get():
    os.environ["BLOG_POST_ROUTE"] = "https://api.hatchways.io/assessment/blog/posts"

    params = {"tag": "tech"}
    res = requests.get(os.getenv("BLOG_POST_ROUTE"), params=params)
    data1 = res.json().get("posts")

    blog = Blog()
    data2 = blog._get(params['tag']).join()

    assert data1 == data2


@pytest.mark.asyncio
async def test_blog_async_get():
    os.environ["BLOG_POST_ROUTE"] = "https://api.hatchways.io/assessment/blog/posts"

    params = {"tag": "tech"}
    res = requests.get(os.getenv("BLOG_POST_ROUTE"), params=params)
    data1 = res.json().get("posts")

    blog = Blog()
    data2 = await blog.get_posts([params['tag']])

    assert data1 == data2
