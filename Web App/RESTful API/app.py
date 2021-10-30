from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with, request, abort, reqparse

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, help="Name should be a string", required=True)
parser.add_argument('roll_no', type=int, help="Roll No should be an integer")
parser.add_argument('country', type=str, help="Country should be a string")

app = Flask(__name__)
api = Api(app)
resource_fields = {
    'full_name': fields.String(attribute='name'),
    'roll_no': fields.Integer,
    'country': fields.String
}


class User:
    def __init__(self, name, roll_no, country):
        self.name = name
        self.roll_no = roll_no
        self.country = country


class FirstResource(Resource):
    @marshal_with(resource_fields)
    def get(self, name):  # Read the resource
        person = User("Shreyash", 78, "India")
        return person

    def post(self, name):  # Create the resource
        args = parser.parse_args()
        f_name = request.form['name']
        roll_no = args['roll_no']
        if type(roll_no) is int:
            abort(400, message="Your roll_no is an integer")
        return f_name

    def put(self, name):  # update the resource
        return "this is put method"

    def delete(self, name):  # delete the resource
        return "this is delete method"


api.add_resource(FirstResource, "/api/<name>")

if __name__ == "__main__":
    app.run(debug=True)
