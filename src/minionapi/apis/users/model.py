from mongoengine import *
from bson import ObjectId

class User(Document):
    user_id = StringField()
    user_name = StringField()
    gender = StringField()
    email = StringField(require=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)
    dob = DateTimeField()

    meta = {'collection': 'users'}


class Users:

    def __init__(self, db):
        self.name = db['name'] if 'name' in db else 'minion'
        self.host = db['host'] if 'host' in db else '127.0.0.1'
        self.port = db['port'] if 'port' in db else 27017
        self.username = db['username'] if 'username' in db else None
        self.password = db['password'] if 'password' in db else None

        connect(db=self.name, host=self.host, port=self.port, username=self.username, password=self.password)

    def get(self, user_id):
        """Retrieve mongodb user record.

        Args:
            user_id (str): user ID

        Returns:
            result (object): mongoengine QuerySet object for user
        """
        try:
            user = User.objects.get(id=user_id)
        except DoesNotExist:
            return None

        return user

    def get_by_email(self, email):
        """Retrieve mongodb user record by email

        Args:
            email (str): email address

        Returns:
            result (object): mongoengine QuerySet object for user
        """
        user = User.objects.get(email=email)
        if user is []:
            return None

        return user

    def get_all(self):
        """Retrieve all mongodb user records

        Returns:
            result (list(object)): list of mongoengine QuerySet objects
        """
        users = [user for user in User.objects()]
        return users

    def insert(self, data):
        """Insert mongodb user record.

        Args:
            data (dict): user data

        Returns:
            result (object): mongoengine QuerySet object for inserted user
        """
        user = User(**data)
        result = user.save()
        return result

    def update(self, data):
        """Update mongodb user record.

        Args:
            data (dict): user data

        Returns:
            result (int): number of records successfully updated
        """
        user = data
        result = User.objects(id=user['id']).update_one(**data)
        return result

    def delete(self, user_id):
        """Delete mongodb user record.

        Args:
            user_id (str): user ID

        Returns:
            result (int): number of records successfully deleted
        """
        try:
            user = User.objects.get(id=user_id)
        except DoesNotExist:
            return 0
        user.delete()
        return 1
