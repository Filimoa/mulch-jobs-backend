from pprint import pformat
from dateutil import parser

from app import db


class Estimate(db.Model):
    """
    Can be mulch, grass cutting, house cleaning, irriggation install
    """

    __tablename__ = "estimate"

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    price = db.Column(
        db.Float,
        nullable=False,
    )
    date = db.Column(db.DateTime)
    note = db.Column(db.String(1000))

    job_type = db.Column(
        db.String(100),
        db.ForeignKey("job_type.name"),
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "job.id",
            ondelete="SET NULL",
        ),
        nullable=True,
    )

    userID = db.Column(db.String(100), db.ForeignKey("user.userID", ondelete="CASCADE"))

    __mapper_args__ = {"polymorphic_identity": "estimate", "polymorphic_on": job_type}

    def __init__(
        self,
        userID: str,
        name: str,
        address: str,
        job_type: str,
        price: float,
        date: str = None,
        note: str = None,
        **kwargs
    ):
        self.userID = userID
        self.name = name
        self.address = address
        self.job_type = job_type
        self.price = price

        self.date = self.parse_date(date)
        self.note = note

    @staticmethod
    def parse_date(date):
        if isinstance(date, str):
            return parser.parse(date)
        return date

    def to_dict(self):
        return {
            "userID": self.userID,
            "name": self.name,
            "address": self.address,
            "job_type": self.job_type,
            "price": self.price,
            "date": self.date,
            "note": self.note,
        }

    def __repr__(self):
        return pformat(self.to_dict())


class MulchEstimate(Estimate):
    __tablename__ = "mulch_estimate"

    id = db.Column(
        db.Integer,
        db.ForeignKey("estimate.id", ondelete="CASCADE"),
        primary_key=True,
    )

    yds = db.Column(
        db.Float,
        nullable=False,
    )

    ft = db.Column(
        db.Float,
        nullable=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "mulching",
    }

    def __init__(self, yds: float = 0, ft: float = 0, zip=0, **kwargs):
        Estimate.__init__(self, **kwargs)

        self.yds = self.get_yds(yds)
        self.ft = ft

    def get_yds(self, yds):
        if yds:
            return yds
        else:
            raise ValueError("MulchEstimate can't have 0 yds")

    @classmethod
    def from_dataframe_row(cls, userID, row):
        return cls(
            userID=userID,
            name=row["name"],
            address=row["address"],
            job_type="mulching",
            price=row["price"],
            date=row["date"],
            note=row["note"],
            yds=row["yds"],
            ft=row["ft"],
        )

    def to_dict(self):
        return {
            **super().to_dict(),
            "yds": self.yds,
            "ft": self.ft,
        }


if __name__ == "__main__":
    pass
