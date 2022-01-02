import json
import pytest
import pydantic.error_wrappers as pyd_errs
from api.models import Post


def test_schema_validation():
    json_schema = json.dumps({
        "title": "Post",
        "description": "Blog post query parameters model",
        "type": "object",
        "properties": {
            "tags": {
                "title": "Tags",
                "anyOf": [
                    {
                        "type": "string"
                    },
                    {
                        "type": "array",
                        "items": {}
                    }
                ]
            },
            "sort_by": {
                "title": "Sort By",
                "default": "id",
                "type": "string"
            },
            "direction": {
                "title": "Direction",
                "default": "asc",
                "type": "string"
            }
        },
        "required": [
            "tags"
        ]
    })

    assert json_schema == Post.schema_json()


def test_tag_validation():
    with pytest.raises(pyd_errs.ValidationError):
        Post()

    with pytest.raises(pyd_errs.ValidationError):
        Post(tags=124)

    with pytest.raises(pyd_errs.ValidationError):
        Post(tags=['hello', "123"])

    post = Post(tags="history,tech,science")
    assert set(post.dict()['tags']) == {"history", "tech", "science"}


def test_sort_by_validation():
    with pytest.raises(pyd_errs.ValidationError):
        Post(tags="history", sort_by="read")

    post = Post(tags="history", sort_by="reads")
    assert post.dict()['sort_by'] == 'reads'


def test_direction_validation():
    with pytest.raises(pyd_errs.ValidationError):
        Post(tags="history", direction="de")

    post = Post(tags="history", direction="desc")
    assert post.dict()['direction'] == 'desc'
