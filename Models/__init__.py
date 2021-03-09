from base_models import JobType, User
from jobs import Config, MulchConfig, MulchJob, GrassJob, Job
from estimates import MulchEstimate, Estimate
from forms import EdgeForm, MulchForm, Form, FormInfo
from typing import Optional

MODEL_NAMES = {
    "config": Config,
    "mulch_config": MulchConfig,
    "mulch_job": MulchJob,
    "grass_job": GrassJob,
    "job": Job,
    "estimate": Estimate,
    "mulch_estimate": MulchEstimate,
    "edge_form": EdgeForm,
    "mulch_form": MulchForm,
    "job_type": JobType,
    "user": User,
    "form_info": FormInfo,
    "form": Form,
}


class ModelMapper:
    def __init__(self, job_type: Optional[str] = None):
        self.job_type = job_type

    @property
    def config(self):
        if self.job_type == "mulching":
            return MulchConfig
        else:
            raise ValueError("Job type {} not found".format(self.job_type))

    @property
    def job(self):
        if self.job_type == "mulching":
            return MulchJob
        else:
            raise ValueError("Job type {} not found".format(self.job_type))

    @property
    def estimate(self):
        if self.job_type == "mulching":
            return MulchEstimate
        else:
            raise ValueError("Job type {} not found".format(self.job_type))

    def get_form_cls(self, form_type):
        if form_type == "mulching_form":
            return MulchForm
        elif form_type == "edging_form":
            return EdgeForm
        else:
            raise ValueError("Form type {} not found".format(form_type))


__all__ = list(MODEL_NAMES.keys())
