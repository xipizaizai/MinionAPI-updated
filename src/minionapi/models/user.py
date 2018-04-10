class User():

    def __init__(self, email, password, first_name, last_name, roles, id=None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.roles = roles
        if id:
            self.id = id

    @classmethod
    def user(cls, user_dict):
        """Initialize User object from user dictionary"""
        user_obj = cls(user_dict['email'],
                       user_dict['password'],
                       user_dict['first_name'],
                       user_dict['last_name'],
                       user_dict['roles'],
                       id=user_dict['id'])

        return user_obj


