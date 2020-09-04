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
        message = args['message']
        splitMessage = message.split()
        colorMapping = {'red': 18, 'blue': 23, 'white': 24, 'green': 25}

        for word in splitMessage[:8]:
            if word.lower() in colorMapping:
                print(colorMapping[word.lower()])
                color = ledPower.LED(colorMapping[word.lower()])
                print("TURNING ON LED", word)
                color.on_off(1)
        return 201

api.add_resource(LED, '/leds')

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
