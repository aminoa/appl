from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import engage

app = Flask(__name__)
api = Api(app)

class Events(Resource):
    def get(self):
        return engage.get_events() 

class Organizations(Resource):
    def get(self):
        return engage.get_organizations() 

class News(Resource):
    def get(self):
        return engage.get_news() 

api.add_resource(Events, "/events")
api.add_resource(Organizations, "/organizations")
api.add_resource(News, "/news")

if __name__ == '__main__':
    app.run()
