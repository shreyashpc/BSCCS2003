from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_name = db.Column(db.String, nullable=False)
    actor_age = db.Column(db.String, nullable=False)
    actor_email = db.Column(db.String, nullable=False, unique=True)


if __name__ == "__main__":
    app.run(debug=True)
