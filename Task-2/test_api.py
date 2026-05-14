import pytest
from pydantic import BaseModel, ValidationError


# pydantic models for schema validation
class Post(BaseModel):
    userId: int
    id: int
    title: str
    body: str


class Comment(BaseModel):
    postId: int
    id: int
    name: str
    email: str
    body: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: str


SCHEMA_MAP = {
    "/posts": Post,
    "/comments": Comment,
    "/users": User
}


def test_fetch_all_posts(get):
    response = get("/posts")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_response_time(get):
    response = get("/posts")
    assert response.elapsed.total_seconds() < 2, (
        f"Response too slow: {response.elapsed.total_seconds():.2f}s"
    )


def test_post_schema(get):
    posts = get("/posts").json()
    for post in posts:
        Post(**post)  # raises ValidationError if schema doesn't match


@pytest.mark.parametrize("endpoint", ["/posts", "/comments", "/users"])
def test_status_code(get, endpoint):
    response = get(endpoint)
    assert response.status_code == 200


@pytest.mark.parametrize("endpoint", ["/posts", "/comments", "/users"])
def test_response_time_all_endpoints(get, endpoint):
    response = get(endpoint)
    elapsed = response.elapsed.total_seconds()
    assert elapsed < 2, f"{endpoint} took {elapsed:.2f}s"


@pytest.mark.parametrize("endpoint", ["/posts", "/comments", "/users"])
def test_schema_validation(get, endpoint):
    items = get(endpoint).json()
    model = SCHEMA_MAP[endpoint]
    for item in items:
        try:
            model(**item)
        except ValidationError as e:
            pytest.fail(f"Schema mismatch on {endpoint}: {e}")


@pytest.mark.parametrize("endpoint", ["/posts", "/comments", "/users"])
def test_returns_list(get, endpoint):
    response = get(endpoint)
    assert isinstance(response.json(), list)