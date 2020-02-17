# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 03:26:10 2020

@author: User
"""

from flask import Flask,render_template,request
import pandas as pd
import numpy as np
app = Flask(__name__, static_url_path="/static",static_folder="static")
data = pd.read_csv("data.csv")
data=data.drop("item_id",axis=1)
data=data.drop("timestamp",axis=1)
movies=data.pivot_table(index="user_id", columns= "title", values= "rating")
movie_list=[]
movie_list1=data["title"]
for i in movie_list1:
    if i not in movie_list:
        movie_list.append(i)
@app.route('/')
def hello_world():
    return render_template("movie_recommend.html")
@app.route("/check_status", methods=["POST","GET"])
def check_status():
    movie_searc = [str(x) for x in request.form.values()]
    for j in movie_searc:
        movie_search=j
    from difflib import get_close_matches
    maine=(get_close_matches(movie_search,movie_list,1,0.2))
    for i in maine:
        maine=i
    main=movies[maine]
    like_movie=movies.corrwith(main)
    like_movie=pd.DataFrame(like_movie, columns=["correlation"])
    y=[]
    for i in (like_movie["correlation"]):
        y.append(i)
    correlation=pd.DataFrame(y)
    raters=pd.DataFrame()
    raters=data.groupby(['title']).size().reset_index(name='raters')
    raters["correlation"]=correlation
    like_movie_=raters
    all_good_correlations=like_movie_[like_movie_["raters"]>100].sort_values("correlation",ascending=False)
    top_correlations=all_good_correlations[all_good_correlations["correlation"]>0.5].sort_values("correlation",ascending=False)
    return render_template("movie_recommend.html",tables=[top_correlations.to_html(classes='data',header="true", table_id="table")], titles=top_correlations.columns.values)
if __name__ =="__main__":
    app.run()