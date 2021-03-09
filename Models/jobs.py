from typing import List
from pprint import pformat

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import Date, cast


from estimates import Estimate, MulchEstimate
from forms import Form, MulchForm, EdgeForm
from app import db


class Config(db.Model):
    __tablename__ = "config"
    __table_args__ = (db.UniqueConstraint("job_type", "userID"),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)

    job_type = db.Column(
        db.String(100),
        db.ForeignKey("job_type.name"),
        nullable=True,
    )

    userID = db.Column(db.String(100), db.ForeignKey("user.userID"))

    hourly_wage = db.Column(
        db.Float,
        nullable=False,
    )
    gross_profit_target = db.Column(
        db.Float,
        nullable=False,
    )
    manager_hourly_wage = db.Column(
        db.Float,
        nullable=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "job_type",
        "polymorphic_on": job_type,
    }

    def __init__(
        self,
        userID: str,
        hourly_wage: float = 0,
        gross_profit_target: float = 0,
        manager_hourly_wage: float = 0,
        **kwargs
    ):
        self.userID = userID
        self.hourly_wage = hourly_wage
        self.manager_hourly_wage = manager_hourly_wage
        self.gross_profit_target = gross_profit_target

    def to_dict(self):
        return {
            "userID": self.userID,
            "hourly_wage": self.hourly_wage,
            "gross_profit_target": self.gross_profit_target,
            "manager_hourly_wage": self.manager_hourly_wage,
        }

    def __repr__(self):
        return pformat(self.to_dict())


class MulchConfig(Config):
    __tablename__ = "mulch_job_config"

    id = db.Column(
        db.Integer,
        db.ForeignKey("config.id", ondelete="CASCADE"),
        primary_key=True,
    )

    wheelbarrows_in_yd = db.Column(
        db.Float,
        nullable=False,
    )
    mulch_cost_per_yd = db.Column(
        db.Float,
        nullable=False,
    )
    revenue_per_yd = db.Column(
        db.Float,
        nullable=False,
    )
    revenue_per_ft = db.Column(
        db.Float,
        nullable=False,
    )

    @declared_attr
    def edge_form_url_id(cls):
        return db.Column(db.String(20), db.ForeignKey("form_info.url_id"))

    @declared_attr
    def mulch_form_url_id(cls):
        return db.Column(db.String(20), db.ForeignKey("form_info.url_id"))

    __mapper_args__ = {
        "polymorphic_identity": "mulching",
    }

    def __init__(
        self,
        job_type: str,
        wheelbarrows_in_yd=0,
        mulch_cost_per_yd=0,
        revenue_per_yd=0,
        revenue_per_ft=0,
        mulch_form_url_id=None,
        edge_form_url_id=None,
        **kwargs
    ):
        Config.__init__(self, **kwargs)
        self.job_type = job_type
        self.wheelbarrows_in_yd = wheelbarrows_in_yd
        self.mulch_cost_per_yd = mulch_cost_per_yd
        self.revenue_per_yd = revenue_per_yd
        self.revenue_per_ft = revenue_per_ft
        self.mulch_form_url_id = mulch_form_url_id
        self.edge_form_url_id = edge_form_url_id

    def to_dict(self):
        return {
            **super().to_dict(),
            "job_type": self.job_type,
            "wheelbarrows_in_yd": self.wheelbarrows_in_yd,
            "mulch_cost_per_yd": self.mulch_cost_per_yd,
            "revenue_per_yd": self.revenue_per_yd,
            "revenue_per_ft": self.revenue_per_ft,
            "mulch_form_url_id": self.mulch_form_url_id,
            "edge_form_url_id": self.edge_form_url_id,
        }


class Job(db.Model):
    """
    A job is composed of a series of forms that get aggregated together once
    the job is completed.

    FIXME make a column called revenue_estimate that's the same as revenue
        # self.revenue_estimate = self.get_revenue_estimate()
    Currently implemented on subclass
    """

    __tablename__ = "job"
    __table_args__ = (db.UniqueConstraint("type", "userID", "address"),)

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address = db.Column(db.String(100), nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    man_hours = db.Column(db.Float)
    labour_cost = db.Column(db.Float)
    material_cost = db.Column(db.Float)
    cost = db.Column(db.Float)
    gross_profit = db.Column(db.Float)
    gross_profit_pct = db.Column(db.Float)
    suggested_price = db.Column(db.Float)
    type = db.Column(
        db.String(50),
        db.ForeignKey("job_type.name"),
    )
    userID = db.Column(db.String(100), db.ForeignKey("user.userID", ondelete="CASCADE"))

    forms = db.relationship("Form", backref="job", lazy="select", cascade="all, delete")

    __mapper_args__ = {"polymorphic_identity": "job", "polymorphic_on": type}

    def __init__(self, estimate: Estimate, forms: Form, config: Config):
        self.forms = self.get_forms(forms)
        self.estimate = estimate
        self.config = config

        # self.form_types = self.get_form_types()
        self.address = self.estimate.address
        self.name = self.estimate.name
        self.price = self.get_price()
        self.userID = config.userID
        self.job_type = config.job_type

        self.man_hours = self.get_man_hours()
        self.labour_cost = self.get_labour_cost()
        self.material_cost = self.get_material_cost()
        self.cost = self.get_cost()
        self.gross_profit = self.get_gross_profit()
        self.gross_profit_pct = self.get_gross_profit_pct()
        self.suggested_price = self.get_suggested_price()

    def get_forms(self, forms):
        if forms:
            return forms
        else:
            raise ValueError("Must have forms completed to create a job summary")

    def get_price(self):
        return self.estimate.price

    def get_man_hours(self):
        return sum([form.man_hours for form in self.forms])

    def get_labour_cost(self):
        return self.man_hours * self.config.hourly_wage

    def get_material_cost(self):
        return 0

    def get_cost(self):
        return self.material_cost + self.labour_cost

    def get_gross_profit(self):
        return self.price - self.labour_cost - self.material_cost

    def get_gross_profit_pct(self):
        return self.gross_profit / self.price

    def get_net_income(self):
        raise NotImplementedError

    def get_net_income_pct(self):
        raise NotImplementedError

    def get_suggested_price(self):
        return self.calc_suggested_price(
            self.price, self.gross_profit, self.config.gross_profit_target
        )

    @staticmethod
    def calc_suggested_price(price: float, gross: float, threshold: float) -> float:
        """
        Creates an updated price to charge someone based on their gross_profit_pct
        and a goal pct

        Params:
            price -> float
            gross -> gross profit, float
            threshold -> float from 0 to 1

        Returns:
            new_price, float
        """
        # meets target
        if gross >= threshold * price:
            return price

        # free job, no price
        if price:
            gross_pct = gross / price
        else:
            gross_pct = -1

        if gross_pct <= 0:
            expense = price + abs(gross)
            new_price = expense / (1 - threshold)
        else:
            expense = price - gross
            new_price = expense / (1 - threshold)

        return new_price

    @property
    def form_types(self):
        """
        Form summary, only unique types
        [{'type': 'edging', 'url_id': '705'}, {'type': 'mulching', 'url_id': '700'}]

        FIXME : Will this ever fail if forms are lazy loaded ?
        """
        form_types = [{"type": form.type, "url_id": form.url_id} for form in self.forms]
        unique = [dict(t) for t in {tuple(d.items()) for d in form_types}]
        return unique

    def to_dict(self):
        return {
            "address": self.address,
            "name": self.name,
            "man_hours": self.man_hours,
            "labour_cost": self.labour_cost,
            "material_cost": self.material_cost,
            "cost": self.cost,
            "gross_profit": self.gross_profit,
            "gross_profit_pct": self.gross_profit_pct,
            "suggested_price": self.suggested_price,
            "price": self.price,
            "form_types": self.form_types,
        }

    def __repr__(self):
        return pformat(self.to_dict())


class MulchJob(Job):
    __tablename__ = "mulch_job"
    # __table_args__ = (db.UniqueConstraint("job_type", "userID"),)

    id = db.Column(
        db.Integer,
        db.ForeignKey("job.id", ondelete="CASCADE"),
        primary_key=True,
    )
    job = relationship(Job, uselist=False, backref="mulch_job", cascade="all, delete")

    revenue_estimate = db.Column(db.Float)
    ft = db.Column(db.Float)
    yds_est = db.Column(db.Float)
    yds_used = db.Column(db.Float)
    yds_extra = db.Column(db.Float)
    mulch_crew_labour_cost = db.Column(db.Float)
    edge_crew_labour_cost = db.Column(db.Float)
    cost_per_yd = db.Column(db.Float)
    cost_per_ft = db.Column(db.Float)
    sprinklers_hit = db.Column(db.Float)
    sprinklers_unfixed = db.Column(db.Float)
    is_cable_cut = db.Column(db.Boolean)
    finish_date = db.Column(db.DateTime)
    crew_lead_edge = db.Column(db.String(100))
    crew_lead_mulch = db.Column(db.String(100))

    estimate = relationship(
        MulchEstimate,
        backref="mulch_job",
        uselist=False,
    )

    __mapper_args__ = {
        "polymorphic_identity": "mulching",
    }

    def __init__(self, estimate: MulchEstimate, forms: List[Form], config: MulchConfig):
        self.mulch_forms, self.edge_forms = self.filter_forms(forms)
        self.config = config
        self.yds_used = self.get_yds_used()

        super().__init__(estimate, forms, config)

        self.ft = self.get_ft()
        self.yds_est = self.get_yds_est()
        self.yds_extra = self.get_yds_extra()
        self.material_cost = self.get_material_cost()
        self.mulch_crew_labour_cost = self.get_mulch_crew_labour_cost()
        self.edge_crew_labour_cost = self.get_edge_crew_labour_cost()
        self.cost_per_yd = self.get_cost_per_yd()
        self.cost_per_ft = self.get_cost_per_ft()
        self.sprinklers_hit = self.get_sprinklers_hit()
        self.sprinklers_unfixed = self.get_sprinklers_unfixed()
        self.is_cable_cut = self.get_is_cable_cut()
        self.finish_date = self.get_finish_date()
        self.crew_lead_edge = self.get_crew_lead_edge()
        self.crew_lead_mulch = self.get_crew_lead_mulch()

        self.revenue_estimate = self.get_revenue_estimate()

    @staticmethod
    def filter_forms(forms):
        """
        Sorts all forms into two seperate lists
            mulch_forms, edge_forms
        """
        edge_forms = []
        mulch_forms = []

        for form in forms:
            if isinstance(form, MulchForm):
                mulch_forms.append(form)
            elif isinstance(form, EdgeForm):
                edge_forms.append(form)
            else:
                raise ValueError(
                    "Unknown form type provided: ", form.__class__.__name__
                )

        if not len(mulch_forms):
            raise ValueError("Mulch job must have forms")

        return mulch_forms, edge_forms

    def get_ft(self):
        return self.estimate.ft

    def get_yds_est(self):
        return self.estimate.yds

    # need to move over yard calculation to here
    def get_yds_used(self):
        return sum(
            [
                form.wheelbarrows / self.config.wheelbarrows_in_yd
                for form in self.mulch_forms
            ]
        )

    def get_yds_extra(self):
        return self.yds_used - self.yds_est

    def get_material_cost(self):
        return self.yds_used * self.config.mulch_cost_per_yd

    def get_mulch_crew_labour_cost(self):
        mulch_man_hours = sum([form.man_hours for form in self.mulch_forms])
        return mulch_man_hours * self.config.hourly_wage

    def get_edge_crew_labour_cost(self):
        edge_man_hours = sum([form.man_hours for form in self.edge_forms])
        return edge_man_hours * self.config.hourly_wage

    def get_cost_per_yd(self):
        return (self.mulch_crew_labour_cost + self.material_cost) / self.yds_est

    def get_cost_per_ft(self):
        if self.ft:
            return self.edge_crew_labour_cost / self.ft
        return 0

    def get_sprinklers_hit(self):
        # FIXME need to add unit test in situation where sprinklers_hit is None
        return sum(
            [form.sprinklers_hit for form in self.edge_forms if form.sprinklers_hit]
        )

    def get_sprinklers_unfixed(self):
        # FIXME need to add unit test in situation where sprinklers_unfixed is None
        return sum(
            [
                form.sprinklers_unfixed
                for form in self.edge_forms
                if form.sprinklers_unfixed
            ]
        )

    def get_is_cable_cut(self):
        return any([form.is_cable_cut for form in self.edge_forms])

    def get_finish_date(self):
        finish_date = None

        for form in self.mulch_forms:
            if form.is_job_done:
                return form.time_end
        return finish_date

    def get_crew_lead_edge(self):
        crew_lead = None
        if self.edge_forms:
            last_edge_form = self.edge_forms[-1]
            crew_lead = last_edge_form.crew_lead

        return crew_lead

    def get_crew_lead_mulch(self):
        last_mulch_form = self.mulch_forms[-1]
        return last_mulch_form.crew_lead

    def get_revenue_estimate(self):
        mulch_revenue = self.yds_used * self.config.revenue_per_yd
        edge_revenue = self.ft * self.config.revenue_per_ft
        return mulch_revenue + edge_revenue

    @staticmethod
    def query_forms(address, userID, filter_date=None):
        mulch_forms = MulchForm.query.filter_by(address=address).filter(
            MulchForm.info.has(userID=userID)
        )

        edge_forms = EdgeForm.query.filter_by(address=address).filter(
            EdgeForm.info.has(userID=userID)
        )

        if filter_date:
            mulch_forms = mulch_forms.filter(
                cast(MulchForm.time_end, Date) == filter_date.date()
            )

            edge_forms = edge_forms.filter(
                cast(EdgeForm.time_end, Date) == filter_date.date()
            )

        mulch_forms = mulch_forms.all()
        edge_forms = edge_forms.all()

        if not mulch_forms:
            raise NoResultFound("Job must have forms completed to create a job summary")

        return mulch_forms, edge_forms

    @classmethod
    def from_address(cls, address, userID, filter_date=None):
        """
        Given form response initializes class by.

        Future:
        Date Param:
            Filters for work completed on date
        """
        # FIXME need to add unit test in situation where estimate does not exist
        mulch_forms, edge_forms = cls.query_forms(address, userID, filter_date)

        job_type = mulch_forms[0].info.job_type

        estimate = (
            MulchEstimate.query.filter_by(address=address)
            .filter_by(job_type=job_type)
            .filter_by(userID=userID)
            .first()
        )

        if not estimate:
            raise NoResultFound(
                "Job {} must have an associated estimate".format(address)
            )

        config = (
            MulchConfig.query.filter_by(userID=userID)
            .filter_by(job_type=job_type)
            .first()
        )

        if not config:
            raise NoResultFound("User {} must have job config".format(userID))

        return cls(
            estimate,
            mulch_forms + edge_forms,
            config,
        )

    def to_dict(self):
        return {
            **super().to_dict(),
            "userID": self.userID,
            "ft": self.ft,
            "yds_est": self.yds_est,
            "yds_used": self.yds_used,
            "yds_extra": self.yds_extra,
            "mulch_crew_labour_cost": self.mulch_crew_labour_cost,
            "edge_crew_labour_cost": self.edge_crew_labour_cost,
            "cost_per_yd": self.cost_per_yd,
            "cost_per_ft": self.cost_per_ft,
            "sprinklers_hit": self.sprinklers_hit,
            "sprinklers_unfixed": self.sprinklers_unfixed,
            "is_cable_cut": self.is_cable_cut,
            "finish_date": self.finish_date,
            "crew_lead_edge": self.crew_lead_edge,
            "crew_lead_mulch": self.crew_lead_mulch,
        }


class GrassJob(Job):
    """
    What's userful to see in a grass job.

    Not sure if finish date makes sense on a grass jopb.

    Looking to be able to query for all jobs finished on a
    """

    __tablename__ = "grass_job"

    id = db.Column(
        db.Integer, db.ForeignKey("job.id", ondelete="CASCADE"), primary_key=True
    )
    finish_date = db.Column(db.DateTime)

    __mapper_args__ = {
        "polymorphic_identity": "grass_cutting",
    }


if __name__ == "__main__":
    pass
