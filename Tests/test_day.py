import pytest
import datetime

from Models import MulchConfig, MulchEstimate, MulchForm, EdgeForm, MulchJob
from day import Day
from mock_data import MockMulchData

mock = MockMulchData(
    new_userID="new",
    new_address="new_address",
    new_mulch_url_id="700",
    new_edge_url_id="705",
)

config = MulchConfig(**mock.config)
estimate = MulchEstimate(**mock.estimate)
mulch_form = MulchForm(
    **mock.mulch_form,
)
edge_form = EdgeForm(**mock.edge_form)
job = MulchJob(estimate, [mulch_form, mulch_form, edge_form], config)


def test_day():
    date = datetime.datetime(2020, 5, 4, 0, 0).date()
    day = Day(date, userID=mock.userID, jobs=[job, job])

    assert day.revenue_estimate == job.revenue_estimate * 2
    assert day._cost == job.cost * 2
    assert day.gross_profit == (job.revenue_estimate - job.cost) * 2
    assert pytest.approx(day.gross_profit_pct, 0.01) == -0.03
    assert day.man_hours == job.man_hours * 2


if __name__ == "__main__":
    test_day()
