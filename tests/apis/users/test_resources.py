import pytest
import json
from bson import ObjectId
from mongoengine import *
from minionapi.app import *
from minionapi.config import TestingConfig
from minionapi.apis.users.model import Users, User


@pytest.fixture(scope='module')
def app(request):
    """Fixture to initialize flask app"""
    app = create_app()

    with app.app_context():
        # init_db()
        yield app


@pytest.fixture
def client(request, app):
    """Fixture to initialize flask-restplus test client"""
    c = app.test_client()

    def teardown():
        pass # os.unlink(app.config['DATABASE'])

    request.addfinalizer(teardown)
    return c


@pytest.fixture(scope='module')
def data(request, app):
    """Fixture to initialize MongoDB test database"""

    cfg = TestingConfig()
    connect('minion-test', host='127.0.0.1')
    _data = {}
    _data['user'] = {}
    user = User()
    user.first_name = "Tyrion"
    user.last_name = "Lannister"
    user.email = "tyrion.lannister.74382147@gmail.com"
    user.gender = "male"
    user.dob = "1994-07-31T00:00:00.000Z"
    result = user.save()
    _data['user']['id'] = str(result.id)
    yield _data
    User.objects.delete()


class TestUsersApi():
    """Tests for users API at /api/users
    These are infrastructure tests and require a running MongoDB instance
    """

    def test_get(self, client, data):
        res = client.get('/api/users')
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_get_by_id(self, client, data):
        uri = '/api/users/' + data['user']['id']
        res = client.get(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_get_by_bad_id(self, client, data):
        uri = '/api/users/' + '356fb7a2c0571b6d6cc2368e'
        res = client.get(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 404

    def test_get_by_email(self, client, data):
        res = client.get('/api/users?tyrion.lannister.74382147@gmail.com')
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_post(self, client, data):
        user = {
            "first_name": "Tom",
            "last_name": "Jones",
            "email": "tim.jones.1877256@gmail.com",
            "gender": "male",
            "dob": "1984-07-31T00:38:21.702Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.post('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_update_by_id(self, client, data):
        user = {
            "id": data['user']['id'],
            "first_name": "Tyrion",
            "last_name": "Lannister",
            "email": "tyrion.lannister.74382147@gmail.com",
            "gender": "female",
            "dob": "1994-07-31T00:00:00.000Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.put('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_update_by_bad_id(self, client, data):
        user = {
            "id": '356fb7a2c0571b6d6cc2368e',
            "first_name": "Tyrion",
            "last_name": "Lannister",
            "email": "tyrion.lannister.74382147@gmail.com",
            "gender": "male",
            "dob": "1994-07-31T00:00:00.000Z"
        }
        user_json = json.dumps(user)
        headers = {'Content-Type': 'application/json'}
        res = client.put('/api/users', data=user_json, headers=headers, follow_redirects=True)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 404

    def test_delete_by_id(self, client, data):
        uri = '/api/users/' + data['user']['id']
        res = client.delete(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 200

    def test_delete_by_bad_id(self, client, data):
        uri = '/api/users/' + '356fb7a2c0571b6d6cc2368e'
        res = client.delete(uri)
        status = res.status_code
        data_bin = res.data
        data = json.loads(data_bin.decode('utf8').replace("'", '"'))

        assert status == 404
