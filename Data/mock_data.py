import datetime
from form_templates import mulch_form_template, edge_form_template

mock_userID = "2e4d705c-5216-4d33-84cb-c96759e3151f"

mock_user = {
    "userID": "test_user",
    "name": "test_name",
    "first_name": "test_first_name",
    "last_name": "test_last_name",
    "phone": "test_phone",
    "email": "test_email",
    "street_address": "test_street_address",
    "city": "test_city",
    "state": "test_state",
    "company_name": "test_company_name",
}

mock_mulch_config = {
    "userID": mock_userID,
    "job_type": "mulching",
    "wheelbarrows_in_yd": 6.3,
    "hourly_wage": 11,
    "manager_hourly_wage": 15,
    "recurring": False,
    "mulch_cost_per_yd": 33.55,
    "gross_profit_target": 0.4,
    "revenue_per_yd": 88.07,
    "revenue_per_ft": 0.78,
    "edge_form_url_id": "705",
    "mulch_form_url_id": "700",
}


mock_edge_form = {
    "url_id": "705",
    "address": "8034 glenmore dr",
    "form_type": "edge_form",
    "crew_lead": "luke",
    "time_start": "5/4/2020 9:00:00",
    "time_end": "5/4/2020 10:00:00",
    "num_ppl": 5,
    "is_job_done": True,
    "sprinklers_hit": 1,
    "sprinklers_unfixed": 1,
    "is_cable_cut": True,
    "job_difficulty": 1,
    "misc_var1": "exists",
    "misc_var2": "exists",
}

mock_mulch_form = {
    "url_id": "700",
    "address": "8034 glenmore dr",
    "form_type": "mulch_form",
    "crew_lead": "mack",
    "time_start": "5/4/2020 9:00:00",
    "time_end": "5/4/2020 10:00:00",
    "num_ppl": 10,
    "is_job_done": True,
    "wheelbarrows": 6.3,
    "job_difficulty": 1,
    "misc_var1": "exists",
    "misc_var2": "exists",
}

mock_mulch_estimate = {
    "userID": "2e4d705c-5216-4d33-84cb-c96759e3151f",
    "name": "sergey filimonov",
    "job_type": "mulching",
    "type": "mulching",  # FIXME
    "address": "8034 glenmore dr",
    "price": 500,
    "date": datetime.datetime.now(),
    "yds": 5,
    "ft": 200,
}

edge_form_info = {
    "url_id": "705",
    "name": "edging_form",
    "job_type": "mulching",
    "display_name": "Mulching Form",
    "userID": "2e4d705c-5216-4d33-84cb-c96759e3151f",
    "template": edge_form_template,
}

mulch_form_info = {
    "url_id": "700",
    "name": "mulch_form",
    "display_name": "Edging Form",
    "job_type": "mulching",
    "userID": "2e4d705c-5216-4d33-84cb-c96759e3151f",
    "template": mulch_form_template,
}


class MockMulchData:
    """
    Class to represent dictionaries of raw data that can
    then be used to create mock objects
    """

    job_type = "mulching"

    def __init__(
        self,
        new_userID,
        new_address,
        new_mulch_url_id,
        new_edge_url_id,
        user=mock_user,
        mulch_config=mock_mulch_config,
        mulch_form=mock_mulch_form,
        edge_form=mock_edge_form,
        mulch_estimate=mock_mulch_estimate,
        mulch_form_info=mulch_form_info,
        edge_form_info=edge_form_info,
    ):
        self.address = new_address
        self.userID = new_userID
        self.edge_form_url_id = new_edge_url_id
        self.mulch_form_url_id = new_mulch_url_id

        self.user = user
        self.config = mulch_config
        self.mulch_form = mulch_form
        self.edge_form = edge_form
        self.estimate = mulch_estimate
        self.mulch_form_info = mulch_form_info
        self.edge_form_info = edge_form_info

        self.all = [
            self.user,
            self.config,
            self.mulch_form,
            self.edge_form,
            self.estimate,
            self.mulch_form_info,
            self.edge_form_info,
        ]

        self.change_userID(new_userID)
        self.change_address(new_address)
        self.change_url_id(
            new_mulch_url_id,
            new_edge_url_id,
        )

    def change_userID(self, userID):
        for dic in self.all:
            if "userID" in dic:
                dic["userID"] = userID

    def change_address(self, address):
        for dic in self.all:
            if "address" in dic:
                dic["address"] = address

    def change_url_id(self, url_id_mulch, url_id_edge):
        edge_obj = [self.edge_form_info, self.edge_form]
        for dic in edge_obj:
            dic["url_id"] = url_id_edge

        mulch_obj = [self.mulch_form_info, self.mulch_form]
        for dic in mulch_obj:
            dic["url_id"] = url_id_mulch

        self.config["edge_form_url_id"] = url_id_edge
        self.config["mulch_form_url_id"] = url_id_mulch
