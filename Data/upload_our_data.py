import pandas as pd
import numpy as np
from dateutil import parser

from Models import MulchEstimate, Estimate, EdgeForm, Form, MulchForm, FormInfo
from app import db

userID = "2e4d705c-5216-4d33-84cb-c96759e3151f"


def remove_formatting(value):
    """
    Cleans formatting from string
    - Remove ',', '$', 'FT', 'YDS' from a value
    - If only whitespace left return 0
    - Convert to int

    Ex '$5,000' -> '5000'
    """
    if isinstance(value, (int, float)):
        return value

    if not value:
        return 0

    formatting = [",", "$", "ft", "yds"]

    value = value.lower()
    for format_type in formatting:
        value = value.replace(format_type, "")

    if value.isspace() or value == "":
        return 0
    return float(value)


def get_mulch_estimates():
    """
    Takes in Diploma mulch estimate csv and outputs a list of MulchEstimate objects!
    """

    df = pd.read_csv(
        "/Users/andreyfilimonov/Coding/mulch-jobs-backend/Data/sample_estimates.csv",
        parse_dates=["date"],
        date_parser=parser.parse,
    )

    df["note"] = None

    df["name"] = df["old_name"].str.lower()
    df["address"] = df["old_address"].str.lower()

    df["mulch"] = df["mulch"].apply(remove_formatting)
    df["edging"] = df["edging"].apply(remove_formatting)
    df["price"] = df["price"].apply(remove_formatting)

    df = df.rename(columns={"edging": "ft", "mulch": "yds"})
    df = df.replace(np.nan, "None", regex=True)

    estimates = []
    for _, row in df.iterrows():
        try:
            estimates.append(MulchEstimate.from_dataframe_row(userID, row))
        except ValueError:
            print("ValueError - failed on: ", row.address)

    return estimates


def get_edge_forms(url_id="705"):
    datetime_cols = [
        "time_start",
        "time_end",
        "timestamp",
    ]

    df = pd.read_csv(
        "/Users/andreyfilimonov/Coding/mulch-jobs-backend/Data/edge_form.csv",
        parse_dates=datetime_cols,
        date_parser=parser.parse,
    )

    UNIQUE_COLS = ["crew_lead", "time_start", "time_end"]
    df = df.drop_duplicates(subset=UNIQUE_COLS)
    df = df.replace({np.nan: None})
    df["url_id"] = url_id

    forms = []
    for row in df.to_dict(orient="records"):
        forms.append(EdgeForm(row))

    return forms


def get_forms(form_type="mulch", url_id="700"):
    # form_type options : "edge" or "mulch"
    datetime_cols = [
        "time_start",
        "time_end",
        "timestamp",
    ]

    df = pd.read_csv(
        "/Users/andreyfilimonov/Coding/mulch-jobs-backend/Data/{}_form.csv".format(
            form_type
        ),
        parse_dates=datetime_cols,
        date_parser=parser.parse,
        dtype={
            "job_finished": bool,
        },
    )

    df = df.replace({np.nan: None})
    df["url_id"] = url_id

    forms = []
    info = FormInfo.query.filter_by(url_id=url_id).first()
    for row in df.to_dict(orient="records"):
        if form_type == "edge":
            forms.append(EdgeForm(row, info=info))
        if form_type == "mulch":
            forms.append(MulchForm(row, info=info))

    return forms


def upload_forms(form_type):
    types = {
        "mulch": {"form_type": "mulch", "url_id": "700"},
        "edge": {"form_type": "edge", "url_id": "705"},
    }

    forms = get_forms(
        form_type=types[form_type]["form_type"], url_id=types[form_type]["url_id"]
    )
    Form.query.filter_by(url_id=types[form_type]["url_id"]).delete()

    db.session.add_all(forms)
    db.session.commit()


def upload_estimates():
    Estimate.query.filter_by(userID=userID).delete()
    estimates = get_mulch_estimates()
    db.session.add_all(estimates)
    db.session.commit()


if __name__ == "__main__":

    db.create_all()

    upload_forms(form_type="edge")

    upload_forms(form_type="mulch")

    upload_estimates()
    # Estimate.query.filter_by(userID=userID).delete()
    # estimates = get_mulch_estimates()
    # db.session.add_all(estimates)
    # db.session.commit()
