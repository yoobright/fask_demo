import logging

from flask import Flask
from flask import jsonify
from flask import got_request_exception
from flask_restful import Resource, Api
from flask_restful import reqparse

from m_math import add_function, div_function

app = Flask(__name__)
api = Api(app)

handler = logging.FileHandler("test.log")  # Create the file logger
logging_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s')
handler.setFormatter(logging_format)
app.logger.addHandler(handler)             # Add it to the built-in logger
app.logger.setLevel(logging.DEBUG)         # Set the log level to debug

def log_exception(sender, exception, **extra):
    """ Log an exception to our logging framework """
    sender.logger.debug('Got exception during processing: %s', exception)

got_request_exception.connect(log_exception, app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


add_parser = reqparse.RequestParser()
add_parser.add_argument('a', type=int, required=True)
add_parser.add_argument('b', type=int, required=True)
add_parser.add_argument('c', type=int)


class Add(Resource):
    def post(self):
        args = add_parser.parse_args()
        app.logger.info("args: {}".format(args))
        a = args.a
        b = args.b
        c = args.c
        result = add_function(a, b, c)
        app.logger.info("result: {}".format(result))
        return jsonify({'result': result})



class Div(Resource):
    def post(self):
        args = add_parser.parse_args()
        app.logger.info("args: {}".format(args))
        a = args.a
        b = args.b
        try:
            result = div_function(a, b)
        except ZeroDivisionError:
            return jsonify({'message': "division by zero"})

        app.logger.info("result: {}".format(result))
        return jsonify({'result': result})

api.add_resource(Add, '/add')
api.add_resource(Div, '/div')

if __name__ == '__main__':
    app.run(debug=True)