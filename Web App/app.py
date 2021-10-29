from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)

class FirstResource(Resource):
    def get(self):  #Read the resource
        return "this is get request"

    def post(self): #Create the resource
        return "this is post method"

    def put(self): #update the resource
        return "this is put method"

    def delete(self):   #delete the resource
        return "this is delete method"


api.add_resource(FirstResource, "/")

if __name__ == "__main__":
    app.run(debug=True)