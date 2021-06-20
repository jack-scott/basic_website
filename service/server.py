from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS, cross_origin
import requests

SE_API_URL = 'https://api.stackexchange.com/2.2'
SE_API_KEY = 'Qz8eMjXBV4vlViTQGXt6fw(('


# defines an endpoint to fetch a list of stackoverflow urls based
# based off a query
class Solutions(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('q', required=True) 
        args = parser.parse_args()
        # for plumbing sake, return queries passed via url

        query_params = {
            'key': SE_API_KEY,
            'site': 'stackoverflow',
            'q': args['q']
        }

        response = requests.get(f'{SE_API_URL}/search/advanced', query_params)
        # un-comment to return full stack overflow response
        # return response.json()

        items = response.json()
        return items

if __name__ == "__main__":
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    api.add_resource(Solutions, '/solutions')

    app.run()