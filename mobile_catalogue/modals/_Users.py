from modals import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True)
    img = db.Column(db.String(120))

    def __init__(self, name, email=None, img=None):
        self.name = name
        self.email = email
        self.img = img
