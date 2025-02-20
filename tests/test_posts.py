from typing import List
from app import schemas


def test_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_all_my_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/my/")

    def validate(post):
        return schemas.PostOut(**post)
    post_map = map(validate, response.json())
    posts = list(post_map)
    #print(posts)
    assert len(response.json()) == len(test_posts)

    assert response.status_code == 200

def test_unauthorized_get_all_my_posts(client):
    response = client.get("/posts/my/")
    assert response.status_code == 401

def test_unauthorized_get_one_my_posts(client):
    response = client.get("/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_unauthorized_get_one_post_does_not_exist(client):
    response = client.get("/posts/0909090}")
    print(response.json())
    assert response.status_code == 401

def test_get_one_my_posts(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    print(post)
    assert post.Post.id == test_posts[0].id
    assert response.status_code == 200

def test_create_post(authorized_client, test_user):
    post_data = {"title": "Post 4", "content": "Content 4"}
    response = authorized_client.post("/posts/", json=post_data)
    post = schemas.ResponsePost(**response.json())
    assert post.title == post_data['title']
    assert post.content == post_data['content']
    assert post.owner_id == test_user['id']
    assert response.status_code == 201

def test_create_post_default_published_true(authorized_client, test_user,test_posts):
    post_data = {"title": "Post 4", "content": "Content 4"}
    response = authorized_client.post("/posts/", json=post_data)
    post = schemas.ResponsePost(**response.json())
    assert post.published == True
    assert response.status_code == 201