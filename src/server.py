# WRDS: Learning words online
# Copyright (C) 2023  Tygo Everts
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from flask import (Flask, render_template, g)
from datetime import datetime
from os import getcwd

if not getcwd().endswith('src'):
    raise OSError("Please cd to src/")

import server.database as db

app = Flask(__name__)


@app.route('/')
def home():
    g.time = int(datetime.now().timestamp())
    return render_template('main.html')


@app.route('/words')
def words():
    index = db.index()
    lists = db.lists()

    list_id = index.search('3.2')[0]
    return lists.get(list_id)


if __name__ == "__main__":
    app.run(debug=True)
