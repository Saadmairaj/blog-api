from api.server import app
from api.utils import remove_duplicates
from fastapi.testclient import TestClient

client = TestClient(app)


def test_ping_good_request():
    res = client.get("/api/ping")

    assert res.status_code == 200
    assert res.json() == {
        "success": True
    }


def test_posts_good_request():
    tag = "tech"
    res = client.get("/api/posts", params={"tags": tag})
    assert res.status_code == 200
    data = res.json().get('posts')

    assert data is not None

    for i in data:
        assert tag in i["tags"]


def test_posts_check_duplicates():
    tag = "tech,history"
    res = client.get("/api/posts", params={"tags": tag})
    assert res.status_code == 200
    data = res.json().get('posts')

    assert data is not None

    data2 = remove_duplicates(list(data))

    assert data == data2


def test_posts_tag_missing():
    res = client.get("/api/posts")
    assert res.status_code == 400

    assert res.json() == {
        "error": "Tags parameter is required"
    }


def test_posts_bad_sort_by_param():
    tag = "tech"
    res = client.get("/api/posts", params={"tags": tag, "sortBy": "tags"})
    assert res.status_code == 400

    assert res.json() == {
        "error": "sortBy parameter is invalid"
    }


def test_posts_bad_direction_param():
    tag = "tech"
    res = client.get("/api/posts", params={"tags": tag, "direction": "a"})
    assert res.status_code == 400

    assert res.json() == {
        "error": "direction parameter is invalid"
    }


def test_posts_check_params():
    tag = "tech"

    for sort_by in ("reads", "likes", "id", "popularity"):
        for d in ("asc", "desc"):
            res = client.get("/api/posts",
                             params={"tags": tag, "sortBy": sort_by, "direction": d})
            assert res.status_code == 200
            data = res.json().get('posts')

            assert data is not None

            val = data[0][sort_by]

            for i in range(1, len(data)):
                if d == 'asc':
                    assert val >= data[i][sort_by]
                else:
                    assert val <= data[i][sort_by]

                val = data[i][sort_by]
