import pytest
from Models import MulchConfig
from mock_data import MockMulchData
from Routes.api_utils import jsonify_single


# pytest Tests/test_api_utils.py -v


@pytest.fixture
def app_context():
    from app import create_app

    app = create_app()

    with app.app_context():
        yield


mock = MockMulchData(
    new_userID="new",
    new_address="new_address",
    new_mulch_url_id="test_mulch_url_id",
    new_edge_url_id="test_edge_url_id",
)


def test_jsonify_single(app_context):
    config = MulchConfig(**mock.config)
    # assert jsonify_single(config) == {"data": config.to_dict(), "status": 200}
