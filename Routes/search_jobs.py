import os
from datetime import datetime

from flask import jsonify, redirect, request, send_from_directory

from app import create_app, db
from errors import bad_request
from Models import Config, Estimate, Form, FormInfo, ModelMapper, User, Job
from api_utils import jsonify_all, jsonify_single, post, upsert

# app = create_app(env="TEST")
app = create_app()
app_context = app.app_context()
app_context.push()
db.create_all()


# === PAGES === #


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")


@app.route("/future", methods=["GET"])
def redirect_to_test():
    return redirect("https://floating-bastion-74887.herokuapp.com/", code=302)


# === FORMS === #


@app.route("/v2/forms/<userID>", methods=["GET"])
def get_forms(userID):
    forms = FormInfo.query.filter_by(userID=userID).all()

    if forms:
        for form in forms:
            form.include_response_summary = True

    return jsonify_all(forms, "forms")


@app.route("/v2/form-template/<url_id>", methods=["GET"])
def get_form_template(url_id):
    form_info = FormInfo.query.filter_by(url_id=url_id).first()
    if not form_info:
        return bad_request("No forms with url_id:{} not found".format(url_id))
    form_info.append_addresses()

    return jsonify_single(form_info, "template")


@app.route("/v2/form-responses/<userID>/<address>/<form_type>", methods=["GET"])
def form_responses(userID, address, form_type):
    # would like to add query for date

    forms = (
        Form.query.join(FormInfo)
        .add_columns(FormInfo.userID)
        .filter(Form.address == address)
        .filter(Form.type == form_type)
        .filter(FormInfo.userID == userID)
        .all()
    )

    return jsonify_all(forms, "form-responses")


@app.route("/v2/form-response/<url_id>", methods=["POST"])
def form_response(url_id: str):
    form_info = FormInfo.query.filter_by(url_id=url_id).first()
    if not form_info:
        return bad_request("No forms found with url_id '{}'".format(url_id))
    form_name = form_info.name

    data = request.get_json()
    data["url_id"] = url_id
    data["timestamp"] = str(datetime.now())  # timezone insensitive
    form_cls = ModelMapper().get_form_cls(form_name)

    return post(form_cls, data)


# === CONFIG=== #


@app.route("/v2/config/<job_type>/<userID>", methods=["GET"])
def get_config(job_type, userID):
    config = Config.query.filter_by(job_type=job_type).filter_by(userID=userID).first()
    return jsonify_single(config)


@app.route("/v2/config/<job_type>/<userID>", methods=["PUT"])
def upsert_config(job_type, userID):
    config_cls = ModelMapper(job_type).config
    config_data = request.get_json()

    return upsert(config_cls, config_data)


# === ESTIMATES === #


@app.route("/v2/estimate/<userID>/<job_type>", methods=["POST"])
def post_estimate(
    userID: str,
    job_type: str,
):
    """
    Returns all estimate user has for a job type
    {"data": [estimate, estimate, ...]}
    """
    estimate_data = request.get_json()
    table = ModelMapper(job_type).estimate
    return post(table, estimate_data)


@app.route("/v2/estimates/<userID>/<job_type>", methods=["GET"])
def get_estimates(userID: str, job_type: str):
    """
    Returns all estimate user has for a job type
    {"data": [estimate, estimate, ...]}
    """
    estimates = (
        Estimate.query.filter_by(userID=userID).filter_by(job_type=job_type).all()
    )
    return jsonify_all(estimates, "estimates")


# === JOBS=== #


@app.route("/v2/jobs/<userID>/<job_type>", methods=["GET"])
def get_job_summary(userID, job_type):
    # query filters
    #    start_date, str : "Apr 1,2020"
    #    end_date, str : "Apr 3,2020"

    query = Job.query.filter_by(userID=userID).filter_by(type=job_type)

    if request.args.get("start_date") and request.args.get("end_date"):
        raise NotImplementedError

    jobs = query.all()
    return jsonify_all(jobs, "jobs")


@app.route("/v2/create-job/<job_type>/<address>/<userID>", methods=["POST"])
def create_job_summary(
    job_type: str,
    address: str,
    userID: str,
):
    job = ModelMapper(job_type).job

    try:
        job = job.from_address(address, userID)
        db.session.add(job)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return bad_request(str(e))

    return jsonify(success=True)


# === DAYS === #


@app.route("/v2/date-summary/<userID>", methods=["GET"])
def get_date_summary(userID):
    # query params: job_type, df
    user = User.query.filter_by(userID=userID).first()
    return jsonify_single(user)


# === USERS === #


@app.route("/v2/user/<userID>", methods=["GET"])
def get_user(userID):
    user = User.query.filter_by(userID=userID).first()
    return jsonify_single(user)


@app.route("/v2/user/<userID>", methods=["PUT"])
def upsert_user(userID):
    user_data = request.get_json()
    return upsert(User, user_data)


# days [GET]
# GET :
# path-params : userID
# return : [daily_summary , daily_summary, ...]

# day [GET]
# GET :
# path-params : userID ,
# query-params : date=None , defaults to most recent day
# returns : {daily-overview: jobs_finished: [job_summary, job_summary ]}


# === CRON === #


# create-daily-summary [GET]
# POST
# params : userID , date
# returns 200

# @app.route("api/v2/job-summary/" ,methods=['PUT'])


if __name__ == "__main__":
    app.run(host="0.0.0.0")
