# WRDS: Learning words online
# Copyright (C) 2024  Tygo Everts
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

from flask import (Flask, render_template)
from os import getcwd

if not getcwd().endswith('src'):
    raise OSError("Please cd to src/")

from server.api import api

app = Flask(__name__)

# For debugging purposes: doesn't save cache
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Register the api
app.register_blueprint(api, url_prefix='/api')


@app.route('/lists/<int:list_id>/test')
def home(list_id: int):
    # Return the word test page
    return render_template('test.html', list_id=list_id)


if __name__ == "__main__":
    # Debug as it is in development
    app.run(debug=True)
