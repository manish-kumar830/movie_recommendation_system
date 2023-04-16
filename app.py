from __future__ import division, print_function
import pickle
from flask import Flask, redirect, url_for, request, render_template
import requests
import pandas as pd
from patsy import dmatrices

movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8e4f3f6efc94cce5b18194960d78de95&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/"+poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key=lambda x: x[1])
    recommended_movie_name = []
    recommended_movie_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_poster.append(fetch_poster(movie_id))
        recommended_movie_name.append(movies.iloc[i[0]].title)
    return recommended_movie_name, recommended_movie_poster




# Define a flask app
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/recommendation', methods=['GET','POST'])
def recommendation():
    movie_list = movies['title'].values
    status = False
    if request.method == "POST":
        
        try:
            if request.form:
                movies_name = request.form['movies']
                recommended_movies_name, recommended_movies_poster = recommend(movies_name)
                status = True
                print(recommended_movies_name)
                return render_template("recommendation.html",movies_name=recommended_movies_name,poster=recommended_movies_poster,movie_list=movie_list,status=status,selected_name=request.form['movies'])
            


        
        except Exception as e:
            error = {'error':e}
            return render_template('recommendation.html',error=error,movie_list=movie_list,status=status)
        
    return render_template('recommendation.html',movie_list=movie_list,status=status)


if __name__ == '__main__':
    app.run(debug=True)