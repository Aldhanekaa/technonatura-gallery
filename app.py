from logging import debug
from flask import Flask, render_template
from flask_pymongo import PyMongo
import os
from dotenv import dotenv_values

config = dict(dotenv_values('.env'))

MONGO_URI: str = ""

try:
    MONGO_URI = os.environ["MONGO_URI"]
except:
    MONGO_URI = "mongodb://127.0.0.1:27017/technonatura-gallery" 


__dirname__ = os.path.dirname(os.path.realpath(__file__))

app = Flask(__name__)
# app.config["MONGO_URI"] = MONGO_URI

# print(app.config.from_object('configmodule.ProductionConfig'))

@app.route("/")
def main_route():
    return render_template('index.html')

@app.route("/login")
def login_route():
    return render_template('login.html')

@app.route("/dashboard")
def main_dashboard_page():
    return render_template('dashboard.html')


data=[
    {
        'name':'Audrin',
        'place': 'kaka',
        'mob': '7736'
    },
    {
        'name': 'Stuvard',
        'place': 'Goa',
        'mob' : '546464'
    }
]


static_markdowns_dir = __dirname__ + '/markdowns'
static_markdowns = os.listdir(static_markdowns_dir)

print(static_markdowns)

for markdown in static_markdowns:
    if markdown.endswith('.md'):
        with open(static_markdowns_dir + '/' + markdown) as f:
            contents = f.read()
            file_name = markdown.replace('.md', '')
            # print(markdown.replace('.md', ''))
            print(file_name)

            @app.route(f"/{file_name.lower()}")
            def privacy_policy():
                return render_template('static_page.html', title=file_name.replace('-', ' '), content=contents)

if __name__ == "__main__":  
    app.run(debug=True)