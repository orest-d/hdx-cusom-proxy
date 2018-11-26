# Example/test service to start a blueprint with custom proxies

import logging
from flask import Flask, Response
import custom_proxy.blueprint as bp

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

app.register_blueprint(bp.app, url_prefix='/custom-proxy')

if __name__ == '__main__':
    app.run(debug=True)
