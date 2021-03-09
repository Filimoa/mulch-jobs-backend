from typing import Dict, List

from flask import jsonify, make_response
from flask_sqlalchemy.model import DefaultMeta as Model
from flask.wrappers import Response

from app import db
from errors import bad_request


def post(table: db.Model, data: Dict) -> Response:
    """
    Post to db given a class name like 'mulch_form' and data to instantiate
    the class.

    Returns:
    ValueError if

    """
    inst = table(**data)
    try:
        inst = table(**data)
        db.session.add(inst)
        db.session.commit()
        return jsonify(success=True)
    except Exception as e:
        print(e)
        db.session.rollback()
        return bad_request(str(e))


def upsert(table: db.Model, data: Dict) -> Response:
    primary_cols = get_unique_contraint_cols(table)
    search_query = {col: data.get(col) for col in primary_cols}
    exists = table.query.filter_by(**search_query).scalar() is not None

    if exists:
        update_data = {key: val for key, val in data.items() if key not in primary_cols}
        inst = table.query.filter_by(**search_query).first()

        for col, val in update_data.items():
            setattr(inst, col, val)

    else:
        inst = table(**data)
        db.session.add(inst)

    db.session.commit()
    return jsonify(success=True)


def serialize_result_obj(res) -> list:
    """
    When performing joins, querying for all() the result is a
    <class 'sqlalchemy.util._collections.result'>. We want to
    serialize this to a regular python dict.

    Model Instances contained in the results are expected to have
    an .as_dict() method to serialize data.
    """
    if issubclass(type(res[0]), tuple):
        payload = []
        for sub_res in res:
            model_instance = list(sub_res._asdict().values())[0]
            payload.append(model_instance.to_dict())
        return payload
    else:
        raise ValueError(
            "Expected <class 'sqlalchemy.util._collections.result'> but passed {}".format(
                type(res)
            )
        )


def jsonify_all(res: List[Model], key: str = "data") -> Response:
    """
    Function to jsonify all results in all query. Assumes res
    """

    if not len(res):
        return make_response({key: {}}, 204)
    # long term would like a better way of dealing with these result obj
    if issubclass(type(res[0]), tuple):
        payload = serialize_result_obj(res)
    else:
        payload = [r.to_dict() for r in res]

    return make_response(
        {key: payload},
        200,
    )


def jsonify_single(res: Model, key: str = "data") -> Response:
    """
    Function to jsonify single Model class.
    """
    payload = res.to_dict() if res else {}
    status = 204 if not res else 200
    return make_response(
        {key: payload},
        status,
    )


def get_unique_contraint_cols(inst: db.Model) -> List[str]:
    """Gets columns in class instance that have a unique
    contraint associated with them.

    Assumptions:
    Only one unqiue contraint exists

    """
    if hasattr(inst, "__table_args__"):
        return inst.__table_args__[0].columns.keys()
    raise ValueError("Model must have primary columns.")
