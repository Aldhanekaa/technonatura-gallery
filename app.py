import os

from flask import Flask, render_template,request, jsonify
from flask_pymongo import PyMongo

from ariadne import QueryType, graphql_sync, make_executable_schema
from ariadne.constants import PLAYGROUND_HTML

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

static_markdowns_dir = __dirname__ + '/markdowns'
static_markdowns = os.listdir(static_markdowns_dir)

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


type_defs = """
    type Query {
        hello: String!
    }
"""

query = QueryType()


@query.field("hello")
def resolve_hello(_, info):
    request = info.context
    user_agent = request.headers.get("User-Agent", "Guest")
    return "Hello, %s!" % user_agent


schema = make_executable_schema(type_defs, query)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    # On GET request serve GraphQL Playground
    # You don't need to provide Playground if you don't want to
    # but keep on mind this will not prohibit clients from
    # exploring your API using desktop GraphQL Playground app.
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    # GraphQL queries are always sent as POST
    data = request.get_json()

    # Note: Passing the request to the context is optional.
    # In Flask, the current request is always accessible as flask.request
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code
    
if __name__ == "__main__":  
    app.run(debug=True)
    print("DEBUG MODE")