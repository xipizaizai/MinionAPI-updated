import pytest
from mongoengine import *
from flask import current_app as app
from minionapi.config import TestingConfig
from minionapi.apis.users.model import Users, User


@pytest.fixture(scope='module')
def db():
    """Fixture to initialize MongoDB test database"""
    cfg = TestingConfig()
    connect('minion-test', host='127.0.0.1')
    data = {}
    user = User()
    user.first_name = "Tyrion"
    user.last_name = "Lannister"
    user.email = "tyrion.lannister.74382147@gmail.com"
    user.gender = "male"
    user.dob = "1994-07-31T00:00:00.000Z"
    result = user.save()
    id = user.pk
    data['user_id'] = str(id)
    data['user'] = user
    data['uri'] = '127.0.0.1'
    data['mongodb'] = cfg.MONGODB
    yield data
    User.objects.delete()


# @pytest.mark.skip
class TestUsersModel():

    def test_init_db(self, db):
        users = Users(db['mongodb'])
        result = users.get(db['user_id'])

        assert result is not None

    def test_get(self, db):
        users = Users(db['mongodb'])
        result = users.get(db['user_id'])
        _users = result.to_json()

        assert result is not None
        assert isinstance(_users, str)

    def test_by_email(self, db):
        users = Users(db['mongodb'])
        result = users.get_by_email(db['user']['email'])

        assert result is not None

    def test_get_all(self, db):
        users = Users(db['mongodb'])
        result = users.get(db['user_id'])

        assert result is not None

    def test_insert(self, db):
        users = Users(db['mongodb'])
        user = {
            "first_name": "John",
            "last_name": "Snow",
            "email": "john.snow.74382147@gmail.com",
            "gender": "male",
            "dob": "1984-07-31T00:38:21.702Z"
        }
        result = users.insert(user)

        assert result is not None

    def test_update(self, db):
        users = Users(db['mongodb'])
        user = {}
        user['first_name'] = "Aegon"
        user['last_name'] = "Targaryen"
        user['id'] = db['user_id']
        result = users.update(user)

        assert result == 1

    def test_delete(self, db):
        users = Users(db['mongodb'])
        result = users.delete(db['user_id'])

        assert result is 1
