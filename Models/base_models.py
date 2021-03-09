from pprint import pformat

from app import db


class JobType(db.Model):
    __tablename__ = "job_type"

    name = db.Column(db.String(100), nullable=False, primary_key=True, unique=True)
    reccurring = db.Column(db.Boolean)

    def __init__(self, name, reccurring):
        self.name = name
        self.reccurring = reccurring

    def __repr__(self):
        return "JobType : {}".format(self.name)


class User(db.Model):
    __tablename__ = "user"

    userID = db.Column(db.String(100), nullable=False, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    street_address = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            "userID": self.userID,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "street_address": self.street_address,
            "city": self.city,
            "state": self.state,
            "company_name": self.company_name,
        }

    def __repr__(self):
        return pformat(self.to_dict())
