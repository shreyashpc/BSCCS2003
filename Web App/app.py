from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Actor(db.Model):
    actor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    actor_name = db.Column(db.String, nullable=False)
    actor_age = db.Column(db.String, nullable=False)
    actor_email = db.Column(db.String, nullable=False, unique=True)
    movies = db.relationship('Association', backref='actor')


class Movie(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String, nullable=False, unique=True)
    release_year = db.Column(db.String, nullable=False)
    dir_name = db.Column(db.String, nullable=False)
    actors = db.relationship('Association', backref='movie')


class Association(db.Model):
    association_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aactor_id = db.Column(db.Integer, db.ForeignKey('actor.actor_id'), nullable=False)
    amovie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable=False)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        name = request.form["Name"]
        age = request.form["age"]
        email = request.form["email"]

        a = Actor(actor_name=name, actor_age=age, actor_email=email)
        db.session.add(a)
        db.session.commit()

        return redirect("/")
    return render_template("form.html")


@app.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        email = request.form['email']
        a = Actor.query.filter_by(actor_email=email).first()
        db.session.delete(a)
        db.session.commit()
        return redirect("/")

    return render_template("delete.html")


@app.route("/addmovie", methods=["GET", "POST"])
def add_movie():
    if request.method == "POST":
        name = request.form['Name']
        director = request.form['director']
        year = request.form['year']
        actor_name = request.form['actor_name']

        # if actor_name == "NA":

        m = Movie(movie_name=name, dir_name=director, release_year=year)
        db.session.add(m)
        db.session.commit()

        m = Movie.query.filter_by(movie_name=name).first()
        a = Association(aactor_id=int(actor_name), amovie_id=int(m.movie_id))
        m.actors.append(a)
        db.session.commit()
        return redirect("/")

    all = Actor.query.all()
    return render_template("addmovie.html", all=all)


if __name__ == "__main__":
    app.run(debug=True)
