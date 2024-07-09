from flask import Flask, render_template,request,redirect
from flask_pymongo import PyMongo
from bson import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo=PyMongo(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hello")
def hello():
    return "hi"

@app.route("/movies")
def movies():
    movies = mongo.db.movies.find()
    return render_template("movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def movieinfo(movie_id):
    movie= mongo.db.movies.find_one({'_id':ObjectId(movie_id)})
    print(movie)
    return render_template("movieinfo.html",movie=movie) 

@app.route('/add_movie')
def add_movie():
    cast_members = mongo.db.cast.find()
    return render_template('add_movie.html', cast_members=list(cast_members))

@app.route('/add_movie', methods=['POST']) 
def add_movie_post(): 
    title = request.form['title'] 
    year = request.form['year'] 
    genre = request.form['genre'] 
    director = request.form.get('director')

    cast_members = request.form.getlist('cast_member')
    roles = request.form.getlist('role')

    cast = []
    for cast_member, role in zip(cast_members, roles):
        cast.append({
            '_id': ObjectId(cast_member),
            'role': role
        })

    movie = {
        'title': title,
        'year': year,
        'genre': genre,
        'director': director,
        'cast': cast,
        'reviews': []
    }

    mongo.db.movies.insert_one(movie)
    return redirect('/movies')
@app.route('/movies/<movie_id>/add_review')
def add_review(movie_id):
    movie = mongo.db.movies.find_one({'_id': ObjectId(movie_id)})
    return render_template('add_review.html', movie=movie)

@app.route('/movies/<movie_id>/add_review', methods=['POST'])
def add_review_post(movie_id):
    user = request.form['user']
    rating = int(request.form['rating'])
    comment = request.form.get('comment')

    review = {
        'user': user,
        'rating': rating,
        'comment': comment
    }

    mongo.db.movies.update_one(
        {'_id': ObjectId(movie_id)},
        {'$push': {'reviews': review}}
    )
    return redirect(f'/movies/{movie_id}/view_reviews')


@app.route('/add_cast')
def add_cast():
    return render_template('add_cast.html')

@app.route('/add_cast', methods=['POST'])
def add_cast_post():
    name = request.form['name']
    date_of_birth = request.form['date_of_birth']

    cast_member = {
        'name': name,
        'date_of_birth': date_of_birth
    }

    mongo.db.cast.insert_one(cast_member)
    return redirect('/cast')
@app.route("/cast")
def cast():
    cast = mongo.db.cast.find()
    return render_template("cast.html", casts=cast)



if __name__ == "__main__":
    app.run(debug=True)
