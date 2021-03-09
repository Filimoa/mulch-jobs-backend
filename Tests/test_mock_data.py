from mock_data import MockMulchData

mock = MockMulchData(
    new_userID="new",
    new_address="new_address",
    new_mulch_url_id="test_mulch_url_id",
    new_edge_url_id="test_edge_url_id",
)


assert mock.address == "new_address"
assert mock.userID == "new"
assert mock.edge_form_url_id == "test_edge_url_id"
assert mock.mulch_form_url_id == "test_mulch_url_id"

assert mock.user["userID"] == "new"
assert mock.config["userID"] == "new"
assert mock.config["edge_form_url_id"] == "test_edge_url_id"
assert mock.config["mulch_form_url_id"] == "test_mulch_url_id"
assert mock.mulch_form["address"] == "new_address"
assert mock.edge_form["address"] == "new_address"
assert mock.mulch_form["url_id"] == "test_mulch_url_id"
assert mock.edge_form["url_id"] == "test_edge_url_id"
assert mock.estimate["address"] == "new_address"
assert mock.estimate["userID"] == "new"
assert mock.edge_form_info["url_id"] == "test_edge_url_id"
assert mock.edge_form_info["userID"] == "new"
assert mock.mulch_form_info["url_id"] == "test_mulch_url_id"
assert mock.mulch_form_info["userID"] == "new"
