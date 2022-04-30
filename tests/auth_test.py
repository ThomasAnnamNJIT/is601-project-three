"""This test the homepage"""
import os

from flask_login import current_user
from werkzeug.datastructures import FileStorage

from app.db.models import User


def test_home_page(client):
    """This makes a request to the home page"""
    response = client.get("/")
    assert response.status_code == 200
    assert b'class="btn btn-primary form-control btn-block"' in response.data
    assert b'type="submit"' in response.data
    assert b'href="/register"' in response.data


def test_dashboard_page(client):
    """This makes a request to the dashboard page"""

    users = User.query.all()
    response = client.get("/dashboard")
    # Assert that the following request is redirected
    assert response.status_code == 302
    # No users are currently in the database (i.e. no user to log in with)
    assert len(users) == 0


def test_user_registration(client):
    """This makes a request to register a user"""

    response = client.post("/register",
                           data=dict(username="test@gmail.com", password="test",
                                     about="This is just a test for about me!!!"))
    assert response.status_code == 302
    users = User.query.all()
    # No users are currently in the database (i.e. no user to log in with)
    assert len(users) == 1
    user = User.query.filter_by(username="test@gmail.com").first()
    assert user.id == 1
    # Since the user id is 1, is_admin should be true
    assert user.is_admin is True
    assert user.authenticated is True
    assert user.about == "This is just a test for about me!!!"
    assert user.password == "test"


def test_user_can_access_dashboard(client):
    """This makes a request to register a user"""

    # Create a newly registered user
    response = client.post("/register",
                           data=dict(username="test@gmail.com", password="test",
                                     about="This is just a test for about me!!!"))
    assert response.status_code == 302

    # Newly registered user is able to log in
    response = client.post("/login", data=dict(username="test@gmail.com", password="test"))
    assert response.status_code == 302
    assert current_user is not None


def test_file_upload(client):
    """This makes a request to upload a file and properly stores within user and song tables"""

    client.post("/register",
                data=dict(username="test@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test@gmail.com", password="test"))

    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "data/random.csv")

    with open(csv_path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="random.csv",
            content_type="text/csv"
        )

        response = client.post("/dashboard",
                               data={"file": my_file},
                               content_type="multipart/form-data")
        assert response.status_code == 200

        assert len(User.query.all())

        user = User.query.filter_by(username="test@gmail.com").first()
        assert user
        assert len(user.songs)
