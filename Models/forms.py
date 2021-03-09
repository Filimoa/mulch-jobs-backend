"""
Not going to worry about incoming data formatting for now. Mostly
concerned about mixed case values.

ID's :
- how are they calculated
- long term shortcomings
"""

from pprint import pformat
from dateutil import parser
from typing import Optional, List, Dict

from sqlalchemy import Sequence
from sqlalchemy.dialects.postgresql import JSON
from app import db
from sqlalchemy.orm import relationship

from estimates import Estimate


class FormInfo(db.Model):
    __tablename__ = "form_info"

    url_id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(100))
    display_name = db.Column(db.String(100))
    job_type = db.Column(db.String(100), db.ForeignKey("job_type.name"))
    userID = db.Column(db.String(100), db.ForeignKey("user.userID"))
    template = db.Column(JSON)

    include_response_summary = False

    def __init__(
        self,
        url_id: str,
        name: str,
        display_name: str,
        job_type: str,
        userID: str,
        template: List[Dict] = [],
    ):
        self.url_id = url_id
        self.name = name
        self.display_name = display_name
        self.job_type = job_type
        self.userID = userID
        self.template = template

    def append_crew_leads(self):
        raise NotImplementedError

    def append_addresses(
        self,
    ) -> None:
        """
        One of the questions on a form will always be the job site address. This
        information is contained in the Estimate table. When requested we need
        to append these options to the to the 'address' question to the question options.

        FIXME: write tests
        """
        if not self.template:
            raise AttributeError("No JSON questions founds in form ")

        addresses = (
            Estimate.query.filter_by(userID=self.userID)
            .filter_by(job_type=self.job_type)
            .with_entities(Estimate.address)
            .all()
        )
        addresses = [address[0] for address in addresses]

        for question in self.template:
            if question.get("id") == "address":
                question.update(options=addresses)

    @property
    def num_questions(self) -> int:
        return len(self.template)

    @property
    def num_responses(self) -> int:
        return Form.query.filter_by(url_id=self.url_id).count()

    @property
    def last_response_date(self) :
        most_recent_form = (
            Form.query.filter_by(url_id="700").order_by(Form.time_end.desc()).first()
        )
        return most_recent_form.time_end

    def to_dict(self):
        # purposely don't include userID
        out = {
            "url_id": self.url_id,
            "name": self.name,
            "job_type": self.job_type,
            "template": self.template,
            "num_questions": self.num_questions,
            "display_name": self.display_name,
        }

        if self.include_response_summary:
            # not usually included since this involves queries
            out["last_response_date"] = self.last_response_date
            out["num_responses"] = self.num_responses

        return out

    def __repr__(self):
        return pformat(self.to_dict())


class Form(db.Model):
    """
    Class to take in represent form responses

    Forms needs to have the primary keys of Job
        - address
        - userID

        But forms only have
        - address
        - url_id (by which you can find userID)
    """

    __tablename__ = "form_response"

    id = db.Column(
        db.Integer,
        Sequence("user_id_seq"),
        primary_key=True,
        server_default=Sequence("user_id_seq").next_value(),
    )
    address = db.Column(
        db.String(100),
        nullable=False,
    )
    timestamp = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    time_start = db.Column(db.DateTime, nullable=False)
    time_end = db.Column(db.DateTime, nullable=False)
    num_ppl = db.Column(db.Integer, nullable=False)
    job_difficulty = db.Column(db.Integer)  # change to str long term
    notes = db.Column(db.Text)
    crew_lead = db.Column(db.String(40))
    is_job_done = db.Column(db.Boolean, nullable=False)
    type = db.Column(db.String(100))  # needs to be foreign key longterm

    url_id = db.Column(
        db.String(20),
        db.ForeignKey("form_info.url_id", ondelete="CASCADE"),
        nullable=False,
    )

    job_id = db.Column(
        db.Integer, db.ForeignKey("job.id", ondelete="SET NULL"), nullable=True
    )
    # job = db.relationship("Job")

    __mapper_args__ = {
        "polymorphic_identity": "form_response",
        "polymorphic_on": type,
    }

    def __init__(
        self,
        address: str,
        time_start: str,
        time_end: str,
        num_ppl: int,
        url_id: str,
        job_difficulty: int = None,
        timestamp: str = None,
        notes: str = None,
        crew_lead: str = None,
        is_job_done: bool = False,
        **kwargs
    ):

        self.address = address
        self.num_ppl = num_ppl
        self.job_difficulty = job_difficulty
        self.notes = notes
        self.crew_lead = crew_lead
        self.is_job_done = self.str2bool(is_job_done)
        self.url_id = url_id

        self.timestamp = self.parse_date(timestamp)
        self.time_start = self.parse_date(time_start)
        self.time_end = self.parse_date(time_end)

    @staticmethod
    def str2bool(v):
        if isinstance(v, bool):
            return bool(v)
        if isinstance(v, str):
            return v.lower() in ("yes", "true", "t", "1")
        else:
            raise ValueError("Unable to parse {} of type {}".format(v, type(v)))

    @staticmethod
    def parse_date(date):
        if isinstance(date, str):
            return parser.parse(date)
        return date

    @property
    def man_hours(self) -> Optional[float]:
        if not self.time_start or not self.time_end or not self.num_ppl:
            return None

        return ((self.time_end - self.time_start) * self.num_ppl).seconds / 3600

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "address": self.address,
            "job_type": self.type,
            "time_start": self.time_start,
            "time_end": self.time_end,
            "num_ppl": self.num_ppl,
            "job_difficulty": self.job_difficulty,
            "notes": self.notes,
            "crew_lead": self.crew_lead,
            "is_job_done": self.is_job_done,
        }

    def __repr__(self):
        return pformat(self.to_dict())


class EdgeForm(Form):
    __tablename__ = "edge_form_response"

    id = db.Column(
        db.Integer,
        db.ForeignKey("form_response.id", ondelete="CASCADE"),
        primary_key=True,
    )

    sprinklers_hit = db.Column(db.Integer)
    sprinklers_unfixed = db.Column(db.Integer)
    is_cable_cut = db.Column(db.Boolean)

    info = relationship(FormInfo, backref="edge_form", cascade="all,delete")

    __mapper_args__ = {
        "polymorphic_identity": "edge_form",
    }

    def __init__(self, sprinklers_hit, sprinklers_unfixed, is_cable_cut, **kwargs):
        Form.__init__(self, **kwargs)
        self.sprinklers_hit = sprinklers_hit
        self.sprinklers_unfixed = sprinklers_unfixed
        self.is_cable_cut = self.str2bool(is_cable_cut)

    def to_dict(self):
        return {
            **super().to_dict(),
            "sprinklers_hit": self.sprinklers_hit,
            "sprinklers_unfixed": self.sprinklers_unfixed,
            "is_cable_cut": self.is_cable_cut,
            "url_id": self.url_id,
        }


class MulchForm(Form):
    __tablename__ = "mulch_form_response"

    id = db.Column(
        db.Integer,
        db.ForeignKey("form_response.id", ondelete="CASCADE"),
        primary_key=True,
    )

    wheelbarrows = db.Column(db.Float, nullable=False)

    info = relationship(FormInfo, backref="mulch_form", cascade="all,delete")

    __mapper_args__ = {
        "polymorphic_identity": "mulch_form",
    }

    def __init__(self, wheelbarrows, **kwargs):
        Form.__init__(self, **kwargs)
        self.wheelbarrows = wheelbarrows

    def to_dict(self):
        return {
            **super().to_dict(),
            "wheelbarrows": self.wheelbarrows,
            "url_id": self.url_id,
        }


if __name__ == "__main__":
    pass

    # db.create_all()
