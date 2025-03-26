import pytest
from app import models

@pytest.fixture()
def test_vote(session,test_posts,test_user):
    new_vote = models.Vote(post_id = test_posts[2].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client,test_posts):
    res = authorized_client.post("/vote/",json = {"post_id":test_posts[2].id, "dir":1})
    assert res.status_code == 201


def test_vote_twice_posts(authorized_client,test_posts,test_vote):
    res = authorized_client.post('/vote/', json = {"post_id":test_posts[2].id, "dir":1})
    assert res.status_code == 409

def test_delete_vote(authorized_client,test_posts,test_vote):
    res= authorized_client.post('/vote/', json = {"post_id":test_posts[2].id, "dir":0})
    assert res.status_code == 201


def test_delete_vote_non_exists(authorized_client,test_posts):
    res= authorized_client.post('/vote/', json = {"post_id":test_posts[2].id, "dir":0})
    assert res.status_code == 404


def test_vote_post_non_exists(authorized_client,test_posts):
    res= authorized_client.post('/vote/', json = {"post_id":1234, "dir":0})
    assert res.status_code == 404

def test_post_vote_un_authorized(client,test_posts):
    res = client.post('/vote/', json = {"post_id":test_posts[2].id, "dir":1})
    assert res.status_code == 401