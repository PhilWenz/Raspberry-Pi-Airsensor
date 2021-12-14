from flask import Flask
from flask_restful import Resource, Api, reqparse
import pymongo
from datetime import datetime

app = Flask(__name__)
api = Api(app)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["RasPiSensor"]
mycol = mydb["Raspi1"]
windows_db = mydb["Windows"]


class Toggle_window_raspi(Resource):
    def patch(self):
        parser = reqparse.RequestParser()
        # parser.add_argument('toggle', required=True)
        parser.add_argument('state', type=bool, required=True)
        args = parser.parse_args()

        data = {
            '$set': {
                'toggle': False, 'state': args['state']}}

        windows_db.update_one({'_id': 'win1'}, data)


class Toggle_Window(Resource):
    def patch(self):
        data = {
            '$set': {
                'toggle': True}}

        windows_db.update_one({'_id': 'win1'}, data)

        return {"msg": "Updated!"}


class Windows(Resource):
    def patch(self):
        parser = reqparse.RequestParser()

        parser.add_argument('auto_toggle', required=True)
        parser.add_argument('temp_threshold', type=float, required=True)
        parser.add_argument('co2_threshold', type=float, required=True)

        args = parser.parse_args()

        data = {
            '$set': {
                'auto_toggle': True if args['auto_toggle'].upper() == 'TRUE' else False,
                'temp_threshold': args['temp_threshold'],
                'co2_threshold': args['co2_threshold']

            }
        }
        windows_db.update_one({'_id': 'win1'}, data)

        return {"msg": "Updated!"}

    def get(self):
        return windows_db.find_one({'_id': 'win1'})


class Data(Resource):

    def put(self):
        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('date', required=True)  # add arguments
        parser.add_argument('co2', type=float, required=True)
        parser.add_argument('temp', type=float, required=True)
        parser.add_argument('tvoc', type=float, required=True)

        args = parser.parse_args()

        # add to DB
        args["_id"] = datetime.fromisoformat(args["date"])

        mycol.insert_one(args)

        return 200

    def get(self):

        parser = reqparse.RequestParser()  # initialize

        parser.add_argument('start_date', required=True)
        parser.add_argument('end_date', required=True)
        parser.add_argument('last', required=True)

        args = parser.parse_args()

        if args["last"].upper() == "TRUE":
            data = mycol.find().sort("_id", -1)[0]
            data['_id'] = data['_id'].isoformat()
            return data

        else:

            all = []
            for data in mycol.find({'_id': {'$gte': datetime.fromisoformat(args['start_date']),
                                            '$lt': datetime.fromisoformat(args['end_date'])}}):
                data['_id'] = data['_id'].isoformat()
                all.append(data)
            return {'data': all}


api.add_resource(Data, '/')
api.add_resource(Windows, '/windows')
api.add_resource(Toggle_Window, '/windows/toggle')
api.add_resource(Toggle_window_raspi, '/windows/toggle/raspi')

if __name__ == '__main__':
    app.run(host="0.0.0.0")
