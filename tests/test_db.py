# Database tests

import unittest
from peewee import *
from app import TimelinePost

MODELS = [TimelinePost]

# use an in-memory SQLite for tests.
test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies.
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step we close
        # the connection...but a good practice all the same.
        test_db.drop_tables(MODELS)

        # Close connection to db.
        test_db.close()

        # If we wanted, we could re-bind the models to their original
        # database here. But for tests this is probably not necessary.

    def test_timeline_post(self):
        # checks timeline posts are properly created
        # .
        # create 2 timeline posts and check that they exists & have the correct id
        first_post = TimelinePost.create(name='John Doe', email="jdoe@example.com", content="Hi, I'm JD")
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Sue', email="jsue@example.com", content="Hi, I'm JS!!")
        assert second_post.id == 2
        # .
        # get timeline posts and assert that they are correct
        first_post_data = TimelinePost.select().where(TimelinePost.id == 1).get()
        assert first_post_data.name == "John Doe"
        assert first_post_data.email == "jdoe@example.com"
        assert first_post_data.content == "Hi, I'm JD"
        second_post_data = TimelinePost.select().where(TimelinePost.id == 2).get()
        assert second_post_data.name == "Jane Sue"
        assert second_post_data.email == "jsue@example.com"
        assert second_post_data.content == "Hi, I'm JS!!"
