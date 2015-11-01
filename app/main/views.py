from flask import render_template
from flask import Response
from . import main
import json


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/search')
def search():
    return render_template('main/search.html')


@main.route('/search/<query>')
def search_query(query):
    data = {
        "results": [
            {
                "title": "Result Title",
                "url": "/optional/url/on/click",
                "image": "optional-image.jpg",
                "price": "Optional Price",
                "description": "Optional Description"
            },
            {
                "title": "Result Title",
                "description": "Result Description"
            }
        ], "action": {
            "url": '/path/to/results',
            "text": "View all 202 results"
        }
    }
    json_data = json.dumps(data)
    return Response(response=json_data, status=200,
                    mimetype="application/json")
