from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import ledPower

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('message')

class LED(Resource):
    def get(self):
        return "hello world"

    def post(self):
        args = parser.parse_args()
        color = args['message']
        print("TURNING ON LED", color)
        colorMapping = {'red': 18, 'blue': 23, 'white': 24, 'green': 25}

        if color in colorMapping:
            print(colorMapping[color])
            color = ledPower.LED(colorMapping[color])
            color.on_off(1)
        
        return 201

api.add_resource(LED, '/leds')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
