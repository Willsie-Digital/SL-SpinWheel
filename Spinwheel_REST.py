from flask import Flask
from flask import render_template
from flask_restful import reqparse, abort, Api, Resource
from pathlib import Path

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('count')

class Nuggets(Resource):
    def post(self):
        args = parser.parse_args()
        _nuggets = args['count']
        _nugget_data_path = Path("REST/")
        f = open(f"{_nugget_data_path}/nuggetsinbound.dat", "w")
        f.write(f"{_nuggets}")
        return f"you posted {_nuggets} nuggets", 201
    
    def get(self):
        _nugget_data_path = Path("REST/")
        f = open(f"{_nugget_data_path}/nuggetsinbound.dat")
        return f.read(), 201



api.add_resource(Nuggets, '/nuggets')

@app.route("/")
def hello():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)