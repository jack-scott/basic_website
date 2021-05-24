from flask import Flask
from flask_restful import Resource, Api, reqparse

# defines an endpoint to fetch a list of stackoverflow urls based
# based off a query
class Solutions(Resource):
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        
        parser.add_argument('q', required=True) 
        args = parser.parse_args()
        # for plumbing sake, return queries passed via url
        print('look ma a server' + args['q'])
        return args['q']

if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Solutions, '/solutions')

    app.run()