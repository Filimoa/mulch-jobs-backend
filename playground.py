# flake8: noqa

from Models import Job, Form, MulchJob, FormInfo, Estimate, User
from Models.schemas import MulchEstimateSchema
from app import create_app, db
import toastedmarshmallow

from Data.mock_data import (
    mock_mulch_config,
    mock_edge_form,
    mock_mulch_form,
    mock_mulch_estimate,
    mock_userID,
)


# app = create_app(env="TEST")
app = create_app()
app_context = app.app_context()
app_context.push()
db.create_all()

import time

# SERIALIZING
# estimate = Estimate.query.filter_by(userID=mock_userID).all()
# estimate = Estimate.query.all()


def query_all_est():
    schema = MulchEstimateSchema()
    schema.jit = toastedmarshmallow.Jit

    # t0 = time.time()
    estimate = Estimate.query.all()
    res = schema.dump(estimate, many=True)


# print("Marshmallow in ", (time.time() - t0))

# estimate = Estimate.query.filter_by(userID=mock_userID).all()
# t0 = time.time()
# for est in estimate:
#     est.to_dict()

# print(".to_dict() in ", (time.time() - t0))

# LOADING

# estimate = MulchEstimateSchema().load(
#     mock_mulch_estimate,
# )

# print(estimate)

# Marshmallow in  6.2
# .to_dict() in  6.336501121520996

if __name__ == "__main__":
    t0 = time.time()
    query_all_est()
    print("Marshamellow in ", (time.time() - t0))

    # cProfile.run("query_all_est()")
