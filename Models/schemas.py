"""
Biggest priority - getting schemas for:
MulchJobConfig
Estimate
MulchForm
EdgeForm
MulchJob
"""
from marshmallow import Schema, fields, validate, post_load
import toastedmarshmallow
from estimates import MulchEstimate


class JobTypeSchema(Schema):
    name = fields.Str()
    recurring = fields.Boolean()


class MulchEstimateSchema(Schema):
    class Meta:
        # unknown = INCLUDE
        jit = toastedmarshmallow.Jit

    userID = fields.Str(required=True)
    type = fields.Str(required=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    address = fields.Str(required=True, validate=validate.Length(min=1))
    job_type = fields.Str(
        required=True,
    )
    price = fields.Number(required=True, validate=validate.Range(min=0))
    date = fields.DateTime(dump_only=True)
    note = fields.Str()
    yds = fields.Number(required=True, validate=validate.Range(min=0))
    ft = fields.Number(required=True, validate=validate.Range(min=0))

    @post_load
    def make_user(self, data, **kwargs):
        return MulchEstimate(**data)
