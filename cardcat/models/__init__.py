from cardcat.database import db
from flask_security import UserMixin, RoleMixin
from flask_security.utils import hash_password
from datetime import datetime


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("user.id"), index=True),
    db.Column("role_id", db.Integer(), db.ForeignKey("role.id"), index=True),
)


class User(db.Model, UserMixin):
    """ User Representation
    Relationships:
    -   A user can have potentially many posts (Specified on `Post` class)
    -   Can comment on many posts. (Specified on `Comment` class)
    -   Has potentially many roles.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(), nullable=False)
    display_name = db.Column(db.String, default="", nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship(
        "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    )

    def __init__(
        self,
        username,
        password,
        email,
        roles=None,
        active=None,
        confirmed_at=None,
        display_name=None,
    ):
        self.username = username
        self.password = hash_password(password)
        if roles:
            self.roles = roles
        self.active = active
        self.confirmed_at = confirmed_at
        self.email = email
        if display_name:
            self.display_name = display_name
        else:
            self.display_name = username

    @property
    def is_admin(self):
        return "admin" in [x.name for x in self.roles]

    # @permalink
    # def absolute_url(self):
    #     return "frontend.user", {"username": self.username}

    def __repr__(self):
        return self.username


class Role(db.Model, RoleMixin):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, index=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    vendor = db.Column(db.String, default='')
    card = db.Column(db.String, nullable=False)
    dttm = db.Column(db.DateTime, default=datetime.now)
    category = db.Column(db.String)
    token = db.Column(db.String, nullable=False, unique=True)
    person = db.Column(db.String)