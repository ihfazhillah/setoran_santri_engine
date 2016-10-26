from flask_login import UserMixin
from flask_credentials import users


class User(UserMixin):

    def __init__(self, id_, username, password):
        self.username = username 
        self.password = password
        self.id = id_


USERS = [User(*x) for x in users]
usernames = {u.username: u.id for u in USERS}
