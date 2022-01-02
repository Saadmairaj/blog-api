from typing import List, Union
from pydantic import BaseModel, validator


class Post(BaseModel):
    """
    Blog post query parameters model
    """

    tags: Union[str, List]
    sort_by: str = "id"
    direction: str = "asc"

    @validator('tags', pre=True, always=True)
    def check_tags(cls, value: str) -> List:
        """Raises ValueError if tags param is null"""
        assert value not in [None, '', ' '], \
            "Tags parameter is required"
        assert isinstance(value, str)
        return list(set([tag for tag in value.split(',') if tag != '']))

    @validator('sort_by', pre=True, always=True)
    def check_sort_by(cls, value: str) -> str:
        """Raises ValueError if the given field is not allowed"""
        assert value in ["id", "reads", "likes", "popularity"], \
            "sortBy parameter is invalid"
        return value

    @validator('direction', pre=True, always=True)
    def check_direction(cls, value: str) -> str:
        """Raises ValueError if the given field is not allowed"""
        assert value in ["asc", "desc"], \
            "direction parameter is invalid"
        return value
