from flask import Flask
import os 
app = Flask(__name__)


@app.route('/')
def hello():
    return '<h1>Hello From Intent Monitor </h1>'


port = int(os.environ.get('PORT', 80))
app.run(debug=True, host='0.0.0.0', port=port)