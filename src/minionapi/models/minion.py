class Minion():

    def __init__(self, minion_name, id=None):
        self.minion_name = minion_name
        if id:
            self.id = id

    @classmethod
    def minion(cls, minion_dict):
        """Initialize Minion object from minion dictionary"""
        minion_obj = cls(minion_dict['minion_name'],
                         id=minion_dict['id'])

        return minion_obj
