from sqlalchemy.orm import validates

from extrapypi.extensions import db


class User(db.Model):
    ROLES = [
        'admin',
        'developer',
        'installer',
        'maintainer'
    ]

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    role = db.Column(db.String(80), nullable=True)

    @validates('role')
    def validate_role(self, key, role):
        assert role in self.ROLES or role is None
        return role

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def email_is_in_use(self):
        q = db.session.query(User.id).filter(User.email == self.email)
        return db.session.query(q.exists()).scalar()

    @property
    def username_is_in_use(self):
        q = db.session.query(User.id).filter(User.username == self.username)
        return db.session.query(q.exists()).scalar()

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return "<User {0.username}>".format(self)
