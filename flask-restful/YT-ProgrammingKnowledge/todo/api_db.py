from flask import Flask
from flask_restful import Resource, Api, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

todos = {
    1: {"task": "Write Hello World Program", "summary": "write a program"},
    2: {"task": "Task 2", "summary": "write a program 2"},
    3: {"task": "Task 3", "summary": "write a program 3"}
}

task_post_args = reqparse.RequestParser()
task_post_args.add_argument("task", type=str, required=True, help="Task is required")
task_post_args.add_argument("summary", type=str, required=True, help="Summary is required")

task_put_args = reqparse.RequestParser()
task_put_args.add_argument("task", type=str)
task_put_args.add_argument("summary", type=str)


class ToDoList(Resource):
    def get(self):
        return todos


class ToDo(Resource):
    def get(self, todo_id):
        return todos[todo_id]

    def post(self, todo_id):
        args = task_post_args.parse_args()
        if todo_id in todos:
            abort(409, "Task ID already exists")
        todos[todo_id] = {"task": args["task"], "summary": args["summary"]}
        return todos[todo_id]

    def put(self, todo_id):
        args = task_put_args.parse_args()
        if todo_id not in todos:
            abort(404, message="Task doesn't exists")
        if args['task']:
            todos[todo_id]['task'] = args['task']
        if args['summary']:
            todos[todo_id]['summary'] = args['summary']
        return todos[todo_id]

    def delete(self, todo_id):
        del todos[todo_id]
        return todos


api.add_resource(ToDo, '/todos/<int:todo_id>')
api.add_resource(ToDoList, '/todos')

if __name__ == '__main__':
    app.run(debug=True)
