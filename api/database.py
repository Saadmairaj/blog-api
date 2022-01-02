import os
from requests import Session
from datetime import timedelta
from typing import Iterable, List
from requests_cache import CachedSession
from api.utils import threaded, wait_until_done, remove_duplicates


class Blog:
    """
    High level wrapper around blog post api endpoint
    """

    def __init__(self) -> None:
        self._route = os.getenv("BLOG_POST_ROUTE")
        self._sess = CachedSession(
            name=f"Blog: {self}",
            cache_control=True,
            expire_after=timedelta(
                minutes=int(os.getenv("CACHE_EXPIRY", 10))
            ),
        ) if os.getenv("CACHING", 'true') in ('true', 'True') else Session()

    @threaded
    def _get(self, tag) -> List:
        """Internal function

        Returns list of all posts related with the given tag"""
        res = self._sess.get(self._route, params={'tag': tag})
        return res.json().get('posts', [])

    async def _sort(self, posts: Iterable, sort_by: str, reverse: bool) -> List:
        """Internal function

        Sorts the list by the given parameter sortBy"""
        return sorted(posts, key=lambda k: k.get(sort_by, ''), reverse=reverse)

    async def get_posts(self, tags: list, sort_by: str = None, direction: str = None):
        """Get all posts from list of tags"""
        direction = True if direction == 'asc' else False
        values = wait_until_done([self._get(tag) for tag in tags])
        values = sum(values, [])

        if not values:
            return values

        posts = remove_duplicates(values)
        if sort_by is None:
            return posts
        return await self._sort(posts, sort_by, direction)

    def close(self):
        """Close Blog session"""
        self._sess.close()

    __del__ = close
