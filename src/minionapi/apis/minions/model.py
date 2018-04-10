from mongoengine import *
from bson import ObjectId

class Minion(Document):
    minion_id = IntField()
    minion_name = StringField()

    meta = {'collection': 'minions'}


class Minions:

    def __init__(self, db):
        self.name = db['name'] if 'name' in db else 'minion'
        self.host = db['host'] if 'host' in db else '127.0.0.1'
        self.port = db['port'] if 'port' in db else 27017
        self.username = db['username'] if 'username' in db else None
        self.password = db['password'] if 'password' in db else None

        connect(db=self.name, host=self.host, port=self.port, username=self.username, password=self.password)

    def get(self, minion_id):
        """Retrieve mongodb minion record.

        Args:
            minion_id (str): minion ID

        Returns:
            result (object): mongoengine QuerySet object for minion
        """
        try:
            minion = Minion.objects.get(id=minion_id)
        except DoesNotExist:
            return None

        return minion

    def get_all(self):
        """Retrieve all mongodb minion records

        Returns:
            result (list(object)): list of mongoengine QuerySet objects
        """
        minions = [minion for minion in Minion.objects()]
        return minions

    def insert(self, data):
        """Insert mongodb minion record.

        Args:
            data (dict): minion data

        Returns:
            result (object): mongoengine QuerySet object for inserted minion
        """
        minion = Minion(**data)
        result = minion.save()
        return result

    def update(self, data):
        """Update mongodb minion record.

        Args:
            data (dict): minion data

        Returns:
            result (int): number of records successfully updated
        """
        minion = data
        result = Minion.objects(id=minion['id']).update_one(**data)
        return result

    def delete(self, minion_id):
        """Delete mongodb minion record.

        Args:
            minion_id (str): minion ID

        Returns:
            result (int): number of records successfully deleted
        """
        try:
            minion = Minion.objects.get(id=minion_id)
        except DoesNotExist:
            return 0
        minion.delete()
        return 1
