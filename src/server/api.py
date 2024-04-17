from flask import Blueprint
from . import database as db

api = Blueprint('api', __name__, url_prefix='/api')


@api.route("/lists/<int:list_id>/words")
def get_list(list_id: int):
    lists = db.lists()

    return lists.get(list_id)
