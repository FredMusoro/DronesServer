from DronesAPI.database.db import db


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String())
    team = db.Column(db.String())

    def __init__(self, username, password, team):
        self.username = username
        self.password = password
        self.team = team

    def json(self):
        return {
            "id": self.id,
            "username": self.username,
            "team": self.team
        }

    # Method to save user to DB
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # Method to remove user from DB
    def remove_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # Class method which finds user from DB by username
    @classmethod
    def find_user_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # Class method which finds user from DB by id
    @classmethod
    def find_user_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    # Class method which lists all users from DB
    @classmethod
    def find_all_users(cls, ):
        return cls.query.all()

    # Class method which lists all users from DB sorted by name
    @classmethod
    def find_users_by_name(cls):
        return cls.query.order_by('username').all()
