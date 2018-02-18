from os.path import join, exists
from json import dumps, load
from pprint import pprint

# 3rd party
from quart import Quart, jsonify, request
from tinydb import TinyDB, Query

app = Quart(__name__)

DB_ROOT = 'db/'
db = TinyDB(join(DB_ROOT, 'database.json'))


@app.route('/')
async def hello():
    return 'Unicorn.io API'


@app.route('/all', methods=['GET'])
def api_dept():
    print(list(db.tables()))
    table = db.table('sequoia-capital')

    return jsonify(table.all()), 200


if __name__ == "__main__":
    app.run(debug=True)