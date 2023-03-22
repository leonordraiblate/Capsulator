from flask import Flask, render_template, request, redirect, url_for
from capsulator_helper import *
import pandas as pd

#Initialize our app
app = Flask(__name__) # I'm creating a flask app in this file

#Create routes (subppages/directories/paths) of our page
@app.route("/", methods = ["GET","POST"])
def index():
    return render_template("index.html")



@app.route("/intro")
def intro():
    return render_template("intro.html")

@app.route("/about_us")
def about_us():
    return render_template("about_us.html")

@app.route("/capsulator",methods = ["GET","POST"])
def capsulator():
    random_pictures, picture_links = random_picture()
    if request.method == "POST":
        # voting = request.form["user_votings"]
        voting1 = request.form["user_votings1"]
        voting2 = request.form["user_votings2"]
        voting3 = request.form["user_votings3"]
        voting4 = request.form["user_votings4"]
        voting5 = request.form["user_votings5"]
        voting6 = request.form["user_votings6"]
        voting7 = request.form["user_votings7"]
        voting8 = request.form["user_votings8"]

        votings=[voting1 ,voting2,voting3,voting4,voting5,voting6,voting7,voting8]

        # ratings= {}
        # for i in list(random_pictures.columns):
        #     ratings[i] = votings[i]

        user_ratings=pd.DataFrame(votings, index=list(random_pictures.columns),columns=["user_rating"])

        user_preferences = ratings(random_pictures,user_ratings)
        global recommended_cloth
        recommended_cloth = recommended_clothes(user_preferences)

        print(recommended_cloth)

#         return render_template("capsulator.html", voting1=voting1, voting2=voting2,voting3=voting3,voting4=voting4,voting5=voting5,voting6=voting6,voting7=voting7,voting8=voting8,random_pictures=random_pictures,picture_links=picture_links)
#     else:
#         return render_template("capsulator.html",random_pictures=random_pictures,picture_links=picture_links)
    

# @app.route("/wardrobe",methods = ["GET","POST"])
# def wardrobe():

#     return render_template("wardrobe.html",recommended_cloth= recommended_cloth)
        return redirect(url_for('wardrobe'))
    else:
        return render_template("capsulator.html",random_pictures=random_pictures,picture_links=picture_links)

@app.route("/wardrobe",methods = ["GET","POST"])
def wardrobe():
    Top, Bottom, Coats, Fullbody ,Footwear,Accessories=recom_categ(recommended_cloth)
    print(Top)
    return render_template("wardrobe.html",recommended_cloth= recommended_cloth,Top=Top, Bottom=Bottom, Coats=Coats, Fullbody=Fullbody,Footwear=Footwear,Accessories=Accessories)


if __name__ == "__main__": #whenever this file "app.py" is called do the following
    app.run(port= 5000,debug=True) #my app will run

    












