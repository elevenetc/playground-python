from flask import Flask
from flask_restful import Api, Resource

from get_manufacturers import get_manufacturers
from get_models import get_models
from get_motorcycles import get_motorcycles


class Motorcycle(Resource):
    def get(self, manufacturer_id, model_id):
        motorcycles = get_motorcycles(manufacturer_id, model_id)
        return motorcycles, 200

class Model(Resource):
    def get(self, manufacturer_id):
        return get_models(manufacturer_id), 200


class Manufacturer(Resource):
    def get(self):
        return get_manufacturers(), 200


app = Flask('motoroccasion')
api = Api(app)
api.add_resource(Manufacturer, '/manufacturers')
api.add_resource(Model, '/models/<string:manufacturer_id>')
api.add_resource(Motorcycle, '/motorcycles/<string:manufacturer_id>/<string:model_id>')

app.run()
