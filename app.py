from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo

# From the separate python file in this directory, we'll import the code that is used to scrape craigslist
import scrape_mars
import sys
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
# mongo = PyMongo(app)

# # identify the collection and drop any existing data for this demonstration
# news = mongo.db.news

# Render the index.html page with any craigslist listings in our database. 
# If there are no listings, the table will be empty.
@app.route("/")
def index():
    collection = db.news
    news_results = collection.find_one()
    print('This is news size', news_results, file=sys.stderr)
    collection = db.figure
    image_url = collection.find_one()
    print('This is image size', image_url, file=sys.stderr)
    collection = db.weather
    weather = collection.find_one()
    print('This is image size', weather, file=sys.stderr)
    collection = db.facts
    facts = collection.find()
    print('This is image size', facts, file=sys.stderr)
    collection = db.hemisphere
    hemispheres = collection.find()
    print('This is hemispheres size', hemispheres, file=sys.stderr)

    # newsArticle = news_results.next()
    # print(newsArticle, file=sys.stderr)

    # for newsAr in news_results:
    #      print("here is the news", newsAr['news_title'], file=sys.stderr)
    return render_template("index.html", news_results=news_results, image_url=image_url, weather=weather, facts=facts, hemispheres=hemispheres)

# This route will trigger the webscraping, but it will then send us back to the index route to render the results
@app.route("/scrape")
def scraper():

    collection = db.news
    collection.drop()
    collection = db.figure
    collection.drop()
    collection = db.weather
    collection.drop()
    collection = db.facts
    collection.drop()
    collection = db.hemisphere
    collection.drop()
    # scrape_craigslist.scrape() is a custom function that we've defined in the scrape_craigslist.py file within this directory
    scrape_mars.scrape()
    
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
