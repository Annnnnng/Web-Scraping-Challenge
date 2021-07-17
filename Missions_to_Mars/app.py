from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Route to render index.html template using data from Mongo
@app.route("/")

def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_data)



# create a route called /scrape that will import scrape_mars.py
@app.route("/scrape")
def scrape():
    mars_info = scrape_mars.scrape_info()

    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)



