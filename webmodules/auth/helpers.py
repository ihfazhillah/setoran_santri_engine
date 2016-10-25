from flask import current_app


class User(object):

    def __init__(self, username, password):
        self.username = username 
        self.password = password

    @classmethod
    def get(cls, username):
        return current_app.config['CREDENTIALS'].get('username')

    @property 
    def is_authenticated(self):
        # try:
        return current_app.config['CREDENTIALS'].get('username') == self.password
        # except KeyError:
            # return False

    @property 
    def is_active(self):
        return self.is_authenticated 

    @property 
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.username
