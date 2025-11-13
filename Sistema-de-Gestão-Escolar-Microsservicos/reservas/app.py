from flask import Flask, jsonify
import logging
from flasgger import Swagger
from database import init_db
from routes import bp as routes_bp
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)
Swagger(app)
db_file = os.environ.get('DB_FILE','reservas.db')
init_db(app, db_file)
app.register_blueprint(routes_bp, url_prefix='/')
@app.route('/')
def index():
    return jsonify({"service":"reservas", "endpoints":["/apidocs","/status"]}), 200
if __name__=='__main__':
    logger.info('Starting reservas service on port 5001')
    app.run(host='0.0.0.0', port=5001)  # Reservas service on port 5001
