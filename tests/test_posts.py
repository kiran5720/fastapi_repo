from app import schemas
import pytest

def test_get_all_posts(authorized_client,test_posts):
    res = authorized_client.get("/posts/")
    # print(res.json())
    # print(authorized_client.headers)
    def validate(post):
        return schemas.PostOut(**post)
    
    post_map = map(validate,res.json())
    list_map = list(post_map)
    assert len(res.json()) == len(test_posts)
    assert res.status_code ==200
    assert list_map[0].Post.id == test_posts[1].id

def test_unauthorized_user_get_all_posts(client,test_posts):
    res = client.get("/posts")
    assert res.status_code == 401

def test_unauthorized_user_get_one_posts(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    print(test_posts[1].__dict__,"ghjk")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client,test_posts):
    res = authorized_client.get("/posts/90")
    assert res.status_code == 404

def test_get_one_post(authorized_client,test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    #print(res.json()["Post"]["owner"])
    post = schemas.PostOut(**res.json())
    print(post)
    assert post.Post.id == test_posts[0].id
    assert post.Post.created_at == test_posts[0].created_at

    # assert res.

@pytest.mark.parametrize("title,content,published",[
    ("first","yenoondu",True),
    ("second","yenoondu",False)])
def test_our_posts(authorized_client,title,content,published):
    res = authorized_client.post("/posts/",json = {"title":title,"content" : content, "published":published})
    post = schemas.Post(**res.json())
    assert post.title == title
    assert res.status_code ==201

def test_unauthorized_delete_posts(client,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    #print(res.status_code)
    assert res.status_code == 401


def test_authorized_delete_posts(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    #print(res.status_code)
    assert res.status_code == 204

def test_authorized_delete_posts_not_exits(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/0098")
    print(res.status_code,"test_authorized_delete_posts_not_exits")
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")
    #print(res.status_code,"test_authorized_delete_posts_not_exits")
    assert res.status_code == 403

def test_update_post(authorized_client,test_posts):
    data = {"title": "rcbbbbbb",
    "content" : "bvctrdsdfres",
    "id":test_posts[0].id}
    res = authorized_client.put(f"/posts/{test_posts[0].id}",json = data)
    update = schemas.Post(**res.json())
    assert res.status_code == 200
    assert update.title == data['title']
    assert update.content == data['content']

def test_update_other_user_post(authorized_client,test_posts,test_user2):
    data = {"title": "rcbbbbbb",
    "content" : "bvctrdsdfres",
    "id":test_posts[2].id}
    res = authorized_client.put(f"/posts/{test_posts[2].id}", json = data)
    assert res.status_code == 403


def test_unauthorized_update_posts(client,test_posts):
    res = client.put(f"/posts/{test_posts[0].id}")
    #print(res.status_code)
    assert res.status_code == 401

def test_authorized_update_posts_not_exits(authorized_client,test_posts):
    data = {"title": "rcbbbbbb",
    "content" : "bvctrdsdfres",
    "id":test_posts[2].id}
    res = authorized_client.put(f"/posts/0098",json = data)
    #print(res.status_code,"test_authorized_delete_posts_not_exits")
    assert res.status_code == 404

