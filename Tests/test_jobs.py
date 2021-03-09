import time
import pytest
from dateutil import parser
import datetime

from Models import (
    MulchConfig,
    MulchEstimate,
    MulchForm,
    MulchJob,
    Form,
    EdgeForm,
    Job,
)

from Data.mock_data import (
    mock_mulch_config,
    mock_edge_form,
    mock_mulch_form,
    mock_mulch_estimate,
)


time0 = time.time()

# ################## #
# CONFIG
# ################## #


# ################## #
# JOBS
# ################## #

mock_mulch_config = MulchConfig(**mock_mulch_config)
estimate = MulchEstimate(**mock_mulch_estimate)
mulch_form = MulchForm(
    **mock_mulch_form,
)
edge_form = EdgeForm(**mock_edge_form)


def test_job_cls():
    job = Job(estimate, [mulch_form, mulch_form, edge_form], mock_mulch_config)

    expected_form_types = [
        {"type": "edge_form", "url_id": "705"},
        {"type": "mulch_form", "url_id": "700"},
    ]
    assert [i for i in job.form_types if i not in expected_form_types] == []

    # FIXME : ADD TESTING FOR CONFIG
    assert job.man_hours == 25
    assert job.labour_cost == 275
    assert job.gross_profit == 225
    assert pytest.approx(job.gross_profit_pct, 0.01) == 0.45

    assert job.calc_suggested_price(100, 50, 0.5) == 100
    assert job.calc_suggested_price(100, 50, 0.2) == 100
    assert job.calc_suggested_price(100, 50, 0.75) == 200
    assert job.calc_suggested_price(100, 60, 0.5) == 100
    assert job.calc_suggested_price(100, 40, 0.5) == 120
    assert job.calc_suggested_price(100, -40, 0.5) == 280
    assert job.calc_suggested_price(100, 0, 0.5) == 200
    assert job.calc_suggested_price(415, 191, 0.6) == 560
    assert pytest.approx(job.calc_suggested_price(100, 0, 0.8), 1) == 500
    assert pytest.approx(job.calc_suggested_price(100, 0, 0.25), 1) == 133


# testing MulchJob class
def test_MulchJob_cls():
    job = MulchJob(
        estimate, [mulch_form, mulch_form, edge_form, edge_form], mock_mulch_config
    )

    assert len(job.edge_forms) == 2
    assert len(job.mulch_forms) == 2

    assert job.labour_cost == 330
    assert job.ft == 200
    assert job.yds_est == 5
    assert job.yds_used == 2
    assert job.yds_extra == -3
    assert job.material_cost == 67.1
    assert job.mulch_crew_labour_cost == 220
    assert job.edge_crew_labour_cost == 110
    assert job.cost_per_yd == (220 + 67.1) / 5
    assert job.cost_per_ft == 110 / 200
    assert job.sprinklers_hit == 2
    assert job.sprinklers_unfixed == 2
    assert job.is_cable_cut

    assert job.finish_date == datetime.datetime(2020, 5, 4, 10, 0)
    assert job.crew_lead_edge == "luke"
    assert job.crew_lead_mulch == "mack"

    assert job.cost == 220 + 67.1 + 110
    assert job.gross_profit == 500 - 220 - 67.1 - 110

    # only worked since we've tested attributes
    assert pytest.approx(job.gross_profit_pct, 0.01) == job.gross_profit / job.price
    assert pytest.approx(job.suggested_price, 0.1) == 661.83
    assert pytest.approx(job.cost_per_yd, 1) == job.mulch_crew_labour_cost / job.yds_est

    assert job.revenue_estimate == job.yds_used * 88.07 + 200 * 0.78

    # no edge forms
    job = MulchJob(estimate, [mulch_form, mulch_form], mock_mulch_config)
    assert job.edge_crew_labour_cost == 0
    assert job.cost_per_ft == 0
    assert job.sprinklers_hit == 0
    assert job.sprinklers_unfixed == 0
    assert not job.is_cable_cut

    # no mulch forms , add tests
    with pytest.raises(ValueError):
        MulchJob(estimate, [edge_form], mock_mulch_config)

    # no forms, errors out
    with pytest.raises(ValueError):
        MulchJob(estimate, [], mock_mulch_config)


# ################## #
# FORMS
# ################## #


def test_forms():
    mulch_form = MulchForm(**mock_mulch_form)
    # edge_form = EdgeForm(**mock_edge_form)

    assert mulch_form.url_id == "700"
    assert mulch_form.wheelbarrows == 6.3

    mulch_form.time_start = parser.parse("7:00:00 AM")
    mulch_form.time_end = parser.parse("8:00:00 AM")
    mulch_form.num_ppl = 1
    assert mulch_form.man_hours == 1

    mulch_form.time_start = parser.parse("11:00:00 AM")
    mulch_form.time_end = parser.parse("1:00:00 PM")
    mulch_form.num_ppl = 1
    assert mulch_form.man_hours == 2

    form = Form(**mock_mulch_form)
    form.time_start = parser.parse("10:00:00 AM")
    form.time_end = parser.parse("11:00:00 AM")
    form.num_ppl = 2
    assert form.man_hours == 2


if __name__ == "__main__":
    test_job_cls()
    test_MulchJob_cls()
    test_forms()
    print("Tests passed in {} seconds! ".format(round(time.time() - time0, 2)))
