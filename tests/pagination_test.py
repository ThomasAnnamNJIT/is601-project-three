"""This tests pagination"""
import os

from werkzeug.datastructures import FileStorage
from app.db.models import User, Song


def test_song_pagination(client):
    """This makes a request to test pagination"""

    client.post("/register",
                data=dict(username="test2@gmail.com", password="test",
                          about="This is just a test for about me!!!"))
    # Newly registered user is able to log in
    client.post("/login", data=dict(username="test2@gmail.com", password="test"))

    root = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(root, "data/testTwo.csv")

    with open(csv_path, "rb") as csv_file:
        my_file = FileStorage(
            stream=csv_file,
            filename="testTwo.csv",
            content_type="text/csv"
        )

        client.post("/dashboard",
                    data={"file": my_file},
                    content_type="multipart/form-data")

        assert len(User.query.all())

        user = User.query.filter_by(username="test2@gmail.com").first()
        assert user
        assert len(user.songs)

    pagination = Song.query.filter_by(user_id=user.id).paginate(1, 5)
    assert len(pagination.items) == 5
    assert pagination.has_next is True
