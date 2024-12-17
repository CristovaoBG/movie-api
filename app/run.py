from flask import Flask
from flask_cors import CORS
from routes import configure_routes 
import routes

print(__name__)
app = Flask(__name__)
CORS(app)

configure_routes(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')