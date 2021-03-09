from estimates import MulchEstimate
from dateutil import parser

# ==============
# ESTIMATES
# ==============


def test_estimate():
    mock_mulch_estimate = {
        "userID": "test_user",
        "name": "sergey filimonov",
        "job_type": "mulching",
        "address": "8034 glenmore dr",
        "price": 500,
        "date": "May 4",
        "yds": 5,
        "ft": 200,
    }

    estimate = MulchEstimate(**mock_mulch_estimate)

    assert estimate.userID == "test_user"
    assert estimate.name == "sergey filimonov"
    assert estimate.address == "8034 glenmore dr"
    assert estimate.job_type == "mulching"
    assert estimate.price == 500
    assert estimate.date == parser.parse("May 4")

    assert estimate.yds == 5
    assert estimate.ft == 200
