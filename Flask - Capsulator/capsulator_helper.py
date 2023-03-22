import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.spatial.distance as dist
import random
from IPython.display import Image, display

categorization_table=pd.read_csv("categorization_table.csv")

images=pd.read_csv("images.csv")

distances = pd.read_csv("distances.csv", index_col="Unnamed: 0")

voting_pictures = pd.read_csv("voting_pictures.csv")

def random_picture():
    x=len(voting_pictures)
    rand_pics_index= random.sample(range(0, x), 8)
    rand_pics=voting_pictures.iloc[rand_pics_index]
    random_pictures=rand_pics
    pictures_items=random_pictures.T.drop(["Picture"]).drop("image link", axis=0)
    picture_links=pd.DataFrame(random_pictures["image link"])
    return pictures_items, picture_links

def votings(random_pictures, picture_links):
    ratings = {}
    for i in list(random_pictures.columns):
        img_url = picture_links.loc[i]["image link"]
        ratings[i] = img_url
    
    # save user ratings to a file
    with open("user_ratings.txt", "a") as f:
        for k, v in ratings.items():
            f.write(f"{k}: {v}\n")
    return ratings

def ratings(random_pictures,voting):
    for i in voting.index:
        i=int(i)
        random_pictures[i]=random_pictures[i]*int(voting["user_rating"].loc[i])
        user_pref=pd.DataFrame(random_pictures.mean(axis=1), columns=['Average'])
        rows_to_drop =user_pref.index[user_pref.eq(0).all(axis=1)]
        user_pref = user_pref.drop(rows_to_drop)
    return user_pref

def recommended_clothes(user_preferences):
    user_clothes = distances.loc[set(user_preferences.index),set(distances.columns).difference(set(user_preferences.index))]
    for name in user_preferences.index:
        user_clothes.loc[name] = user_clothes.loc[name]*user_preferences.loc[name].values[0]
    recommended_cloth=pd.DataFrame(user_clothes.sum().sort_values(ascending=False))
    return recommended_cloth

def recom_categ(recommended_clothes):
    recommendations=pd.DataFrame(recommended_clothes).reset_index().reset_index()
    recommendations.columns = ["Rating","Item","Score"]
    recommendations["Rating"]=recommendations["Rating"]+1
    recommendations = recommendations[recommendations["Score"]>0].drop(columns=["Score"])
    recommendations_categories = pd.merge(left=recommendations,
                               right = categorization_table,
                               how = "inner",
                               left_on = "Item",
                               right_on = "Items")
    recommendations_categ=recommendations_categories.drop("Items",axis=1)
    recommendations_categ_img= pd.merge(left=recommendations_categ,
                               right = images,
                               how = "inner",
                               left_on = "Item",
                               right_on = "Items")
    recommendations_categ_img.drop("Items",axis=1,inplace=True)
    grouped = recommendations_categ_img.groupby('Category')
    dfs = {}
    for name, group in grouped:
        dfs[name] = group.copy()
    for name, df in dfs.items():
        print(f"Dataframe for Category: {name}")
        print(df.head())  
    return dfs["Top"], dfs["Bottom"], dfs["Coats"], dfs["Fullbody"], dfs["Footwear"], dfs["Accessories"]  

