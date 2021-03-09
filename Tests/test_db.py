import pytest
import datetime

from typing import Callable
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from base_models import User, JobType
from forms import FormInfo, MulchForm, EdgeForm, Form
from estimates import MulchEstimate, Estimate
from jobs import MulchJob, Config, MulchConfig, Job

from mock_data import MockMulchData

# pytest Tests/test_db.py -v
# pytest Tests/test_db.py::Test_Job::test_create_job_from_address_userID -v

# ========================= #
# ------- FIXTURES -------- #
# ========================= #


@pytest.fixture(scope="module")
def mock_mulch_data():
    mock = MockMulchData(
        new_userID="test_user",
        new_address="test_address",
        new_mulch_url_id="test_mulch_url_id",
        new_edge_url_id="test_edge_url_id",
    )
    return mock


@pytest.fixture(scope="class")
def parent_child(db, mock_mulch_data):
    mock = mock_mulch_data
    return [
        {
            "parent": Config,
            "child": MulchConfig,
            "data": mock.config,
            "delete_query": Config.query.filter_by(job_type="mulching")
            .filter_by(userID=mock.userID)
            .delete,
        },
        {
            "parent": Estimate,
            "child": MulchEstimate,
            "data": mock_mulch_data.estimate,
            "delete_query": Estimate.query.filter_by(address=mock.address)
            .filter_by(job_type="mulching")
            .filter_by(userID=mock.userID)
            .delete,
        },
    ]


@pytest.fixture(scope="class")
def db(mock_mulch_data):
    from app import create_app, db

    app = create_app(env="TEST")
    app_context = app.app_context()
    app_context.push()
    db.drop_all()
    db.create_all()

    # inserts some sample data into the database
    job_type = JobType(name="mulching", reccurring=False)
    db.session.add(job_type)
    db.session.commit()
    user = User(**mock_mulch_data.user)
    db.session.add(user)
    db.session.commit()
    mulch_form_info = FormInfo(**mock_mulch_data.mulch_form_info)
    edge_form_info = FormInfo(**mock_mulch_data.edge_form_info)

    db.session.add_all([mulch_form_info, edge_form_info])
    db.session.commit()

    # only when cleanup wasn't performed
    # db.session.remove()
    # db.drop_all()

    yield db

    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="class")
def insert_mulch_job(db, mock_mulch_data):
    config = MulchConfig(**mock_mulch_data.config)
    estimate = MulchEstimate(**mock_mulch_data.estimate)
    mulch_form_1 = MulchForm(
        **mock_mulch_data.mulch_form,
    )
    mulch_form_2 = MulchForm(
        **mock_mulch_data.mulch_form,
    )
    edge_form_1 = EdgeForm(**mock_mulch_data.edge_form)
    edge_form_2 = EdgeForm(**mock_mulch_data.edge_form)

    objs = [config, estimate, mulch_form_1, mulch_form_2, edge_form_1, edge_form_2]
    db.session.add_all(objs)
    db.session.commit()

    job = MulchJob.from_address(mock_mulch_data.address, mock_mulch_data.userID)
    db.session.add(job)
    db.session.commit()

    yield

    # delete job


# ========================= #
# --------- TESTS --------- #
# ========================= #


class Test_Row_Inserts:
    """
    Adds data to databse assuming nothing interferes, cleanup
    not done until all class functions run.
    """

    def test_adding_user(self, db, mock_mulch_data):
        data = mock_mulch_data.user.copy()
        data.update(
            {
                "userID": "test_adding_user",
                "name": "test_adding_user",
                "company_name": "test_adding_user",
            }
        )

        user = User(**data)
        db.session.add(user)
        db.session.commit()

    def test_adding_forms(self, db, mock_mulch_data):
        form_info = FormInfo.query.filter_by(
            url_id=mock_mulch_data.config["edge_form_url_id"]
        ).first()

        mulch_form = MulchForm(**mock_mulch_data.mulch_form, forms=form_info)
        db.session.add(mulch_form)
        db.session.commit()

        edge_form = EdgeForm(**mock_mulch_data.edge_form, forms=form_info)
        db.session.add(edge_form)
        db.session.commit()

        Form.query.filter_by(address="test_adding_forms").delete()
        db.session.commit()

    def test_adding_estimates(self, db, mock_mulch_data):
        estimate = MulchEstimate(**mock_mulch_data.estimate)
        db.session.add(estimate)
        db.session.commit()


class Test_DB_Behaviour_1:
    @staticmethod
    def assert_only_one_insert_possible(db, child, data, delete_query, **kwargs):
        delete_query()
        db.session.commit()

        child_inst = child(**data)
        db.session.add(child_inst)
        db.session.commit()

        with pytest.raises(IntegrityError):
            child_inst = child(**data)
            db.session.add(child_inst)
            db.session.commit()

    def test_only_one_insert_possible_config(self, db, mock_mulch_data):
        args = {
            "child": MulchConfig,
            "data": mock_mulch_data.config,
            "delete_query": Config.query.filter_by(job_type="mulching")
            .filter_by(userID=mock_mulch_data.userID)
            .delete,
        }

        self.assert_only_one_insert_possible(db, **args)


@pytest.mark.usefixtures("db", "parent_child")
class Test_DB_Behaviour_2:
    @staticmethod
    def assert_deleting_parent_also_deletes_child(
        db, parent, child, data: dict, delete_query: Callable
    ):
        # these 3 lines should be refactored out of here
        child_inst = child(**data)
        db.session.add(child_inst)
        db.session.commit()

        parent_nrows_start = db.session.query(parent).count()
        child_nrows_start = db.session.query(child).count()

        delete_query()
        db.session.commit()

        parent_nrows_end = db.session.query(parent).count()
        child_nrows_end = db.session.query(child).count()

        assert parent_nrows_end == parent_nrows_start - 1
        assert child_nrows_end == child_nrows_start - 1

    def test_deleting_Config_deletes_MulchConfig(self, db, mock_mulch_data):
        vars = {
            "parent": Config,
            "child": MulchConfig,
            "data": mock_mulch_data.config,
            "delete_query": Config.query.filter_by(job_type="mulching")
            .filter_by(userID=mock_mulch_data.userID)
            .delete,
        }

        self.assert_deleting_parent_also_deletes_child(db, **vars)

    def test_deleting_Estimate_deletes_MulchEstimate(self, db, mock_mulch_data):
        vars = {
            "parent": Estimate,
            "child": MulchEstimate,
            "data": mock_mulch_data.estimate,
            "delete_query": Estimate.query.filter_by(address=mock_mulch_data.address)
            .filter_by(job_type="mulching")
            .filter_by(userID=mock_mulch_data.userID)
            .delete,
        }

        self.assert_deleting_parent_also_deletes_child(db, **vars)

    def test_deleting_Job_deletes_MulchJob(self, db, mock_mulch_data, insert_mulch_job):
        # since adding a job isn't as simple as initializing a Job object

        parent_nrows_start = db.session.query(Job).count()
        child_nrows_start = db.session.query(MulchJob).count()

        Job.query.filter_by(address=mock_mulch_data.address).filter_by(
            type="mulching"
        ).filter_by(userID=mock_mulch_data.userID).delete()

        db.session.commit()

        parent_nrows_end = db.session.query(Job).count()
        child_nrows_end = db.session.query(MulchJob).count()

        assert parent_nrows_end == parent_nrows_start - 1
        assert child_nrows_end == child_nrows_start - 1


class Test_Job:
    def test_create_job_from_address_userID(self, db, mock_mulch_data):
        config = MulchConfig(**mock_mulch_data.config)
        estimate = MulchEstimate(**mock_mulch_data.estimate)
        mulch_form_1 = MulchForm(
            **mock_mulch_data.mulch_form,
        )
        mulch_form_2 = MulchForm(
            **mock_mulch_data.mulch_form,
        )
        edge_form_1 = EdgeForm(**mock_mulch_data.edge_form)
        edge_form_2 = EdgeForm(**mock_mulch_data.edge_form)

        objs = [config, estimate, mulch_form_1, mulch_form_2, edge_form_1, edge_form_2]
        db.session.add_all(objs)
        db.session.commit()

        # 4 , directly from test_jobs.py
        job = MulchJob.from_address(mock_mulch_data.address, mock_mulch_data.userID)
        db.session.add(job)
        db.session.commit()

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

        Job.query.filter_by(address=mock_mulch_data.address).delete()
        db.session.commit()

    def test_create_job_from_date_filter(self, db, mock_mulch_data):
        # only mulch form date is changed
        form = MulchForm.query.filter_by(address=mock_mulch_data.address).first()
        form.time_end = form.time_end + datetime.timedelta(days=1)
        db.session.commit()

        job = MulchJob.from_address(
            mock_mulch_data.address,
            mock_mulch_data.userID,
            datetime.datetime(2020, 5, 4, 10, 0),
        )

        assert len(job.edge_forms) == 2
        assert len(job.mulch_forms) == 1
        assert job.mulch_crew_labour_cost == 110

        Job.query.filter_by(address=mock_mulch_data.address).delete()
        db.session.commit()

        # edge form data also changed
        form = EdgeForm.query.filter_by(address=mock_mulch_data.address).first()
        form.time_end = form.time_end + datetime.timedelta(days=1)
        db.session.commit()

        job = MulchJob.from_address(
            mock_mulch_data.address,
            mock_mulch_data.userID,
            datetime.datetime(2020, 5, 4, 10, 0),
        )

        assert len(job.edge_forms) == 1
        assert len(job.mulch_forms) == 1
        assert job.edge_crew_labour_cost == 55

        Job.query.filter_by(address=mock_mulch_data.address).delete()
        db.session.commit()

        # make sure error happens if invalid date
        with pytest.raises(NoResultFound):
            WRONG_YEAR = 1776
            job = MulchJob.from_address(
                mock_mulch_data.address,
                mock_mulch_data.userID,
                datetime.datetime(WRONG_YEAR, 5, 4, 10, 0),
            )

        Job.query.filter_by(address=mock_mulch_data.address).delete()
        db.session.commit()

    def test_forms_est_exist_after_deleting_job(self, db, mock_mulch_data):
        """
        Looking to make sure forms, estimate still exists even if we delete a job
        """
        job = MulchJob.from_address(
            mock_mulch_data.address,
            mock_mulch_data.userID,
        )
        db.session.add(job)
        db.session.commit()

        # job = MulchJob.query.filter_by(address=mock_mulch_data.address).first()
        Job.query.filter_by(address=mock_mulch_data.address).delete()
        db.session.commit()

        # test intialization still works
        job = MulchJob.from_address(
            mock_mulch_data.address,
            mock_mulch_data.userID,
        )

        assert len(job.forms) == 4
