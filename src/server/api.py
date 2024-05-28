# WRDS: Learning words online
# Copyright (C) 2024  Tygo Everts
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import Blueprint
from . import database as db

api = Blueprint('api', __name__)


@api.route("/lists/<int:list_id>/words")
def get_list(list_id: int):
    """Returns words in json form"""
    lists = db.lists()

    return lists.get(list_id)


@api.route('/lists/<int:list_id>/meta')
def get_meta(list_id: int):
    """Returns metadata about a list"""
    index = db.index()

    return index.get(list_id)


@api.route('/lists')
def get_lists():
    """Return all lists"""
    index = db.index()

    return index.list()
