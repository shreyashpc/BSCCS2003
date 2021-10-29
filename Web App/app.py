from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

class FirstResource(Resource):
    def get(self, name):  #Read the resource
        return f"hello {name}", 200, {"This is a header": "the 3rd parameter"}

    def post(self, name): #Create the resource
        return "this is post method"

    def put(self, name): #update the resource
        return "this is put method"

    def delete(self, name):   #delete the resource
        return "this is delete method"


api.add_resource(FirstResource, "/api/<name>")

if __name__ == "__main__":
    app.run(debug=True)