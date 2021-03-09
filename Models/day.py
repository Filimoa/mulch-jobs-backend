from pprint import pformat

# from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Date, cast

from app import db
from jobs import MulchJob


class Day:
    """
    Needs to be able to handle a variety
    of jobs types.

    Want to have all job linked to this

    """

    date = db.Column(db.DateTime, nullable=True, primary_key=True)
    userID = db.Column(db.String(100), db.ForeignKey("user.userID"), primary_key=True)

    revenue_estimate = db.Column(db.Float)
    gross_profit = db.Column(db.Float)
    gross_profit_pct = db.Column(db.Float)
    hours_worked = db.Column(db.Float)
    num_jobs_finished = db.Column(db.Integer)

    def __init__(self, date, userID, jobs):
        self.date = date
        self.userID = userID
        self.jobs = jobs

        self.revenue_estimate = self.get_revenue_estimate()
        self.gross_profit = self.get_gross_profit()
        self.gross_profit_pct = self.get_gross_profit_pct()
        self.man_hours = self.get_man_hours()
        self.num_jobs_finished = self.get_num_jobs_finished()

    def get_revenue_estimate(self):
        return sum([job.revenue_estimate for job in self.jobs])

    @property
    def _cost(self):
        return sum([job.cost for job in self.jobs])

    def get_gross_profit(self):
        return self.revenue_estimate - self._cost

    def get_gross_profit_pct(self):
        return self.gross_profit / self.revenue_estimate

    def get_man_hours(self):
        return sum([job.man_hours for job in self.jobs])

    def get_num_jobs_finished(self):
        # FIXME
        return sum(1 for e in self.jobs if e.finish_date == self.date)

    @classmethod
    def from_date(cls, date, userID: str):
        # want to be able to give it a date and userID and it sums up all jobs
        # need to have table with userID, address, job_type,

        mulch_jobs = MulchJob.query.filter(MulchJob.info.has(userID=userID))

        mulch_jobs = mulch_jobs.filter(cast(MulchJob.time_end, Date) == date.date())

    def to_dict(self):
        return {
            "revenue_estimate": self.revenue_estimate,
            "cost": self._cost,
            "gross_profit": self.gross_profit,
            "gross_profit_pct": self.gross_profit_pct,
            "man_hours": self.man_hours,
            "num_jobs_finished": self.num_jobs_finished,
        }

    def __repr__(self):
        return pformat(self.to_dict())


# looking to have these derived from forms associated with day
class MulchCrewDay:
    """
    Looking to know

    yds
    mulch_cost
    labour_cost
    total_cost

    Input is jobs
    """

    def __init__(self, date, userID, jobs):
        pass

    @classmethod
    def from_date(cls, date, userID: str):
        pass


class EdgeCrewDay:
    """
    Looking to know

    yds
    mulch_cost
    labour_cost
    total_cost
    """

    def __init__(self, date, userID, jobs):
        pass

    @classmethod
    def from_date(cls, date, userID: str):
        pass


if __name__ == "__main__":
    pass
