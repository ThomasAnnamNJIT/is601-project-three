"""This test user model"""

import logging

from app import db
from app.db.models import User, Song


def test_adding_user(application):
    """This tests a user is added"""
    log = logging.getLogger("myApp")
    with application.app_context():
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0
        # showing how to add a record
        # create a record
        user = User('keith@webizly.com', 'testtest', "This tests that an about section is created")
        # add it to get ready to be committed
        db.session.add(user)
        # call the commit
        # db.session.commit()
        # assert that we now have a new user
        # assert db.session.query(User).count() == 1
        # finding one user record by email
        user = User.query.filter_by(username='keith@webizly.com').first()
        log.info(user)
        # asserting that the user retrieved is correct
        assert user.username == 'keith@webizly.com'
        # this is how you get a related record ready for insert
        user.songs = [Song("test", "smap", 2022, "Rap"), Song("test2", "te", 2003, "Country")]
        # commit is what saves the songs
        db.session.commit()
        assert db.session.query(Song).count() == 2
        song1 = Song.query.filter_by(title='test').first()
        assert song1.title == "test"
        # changing the title of the song
        song1.title = "SuperSongTitle"
        # saving the new title of the song
        db.session.commit()
        song2 = Song.query.filter_by(title='SuperSongTitle').first()
        assert song2.title == "SuperSongTitle"
        # checking cascade delete
        db.session.delete(user)
        assert db.session.query(User).count() == 0
        assert db.session.query(Song).count() == 0


def test_edit_user(client):
    """This makes a request to edit a user"""
    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302

    response = client.get("/users/edit")
    assert response.status_code == 200
    password = "new_password"
    about = "Test to see if I can edit"

    response = client.post("/users/edit",
                           data=dict(username="test@gmail.com", password=password,
                                     about=about))
    assert response.status_code == 200

    user = User.query.filter_by(username="test@gmail.com").first()
    assert user.password == password
    assert user.about == about
