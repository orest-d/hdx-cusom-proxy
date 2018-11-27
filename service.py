# Example/test service to start a blueprint with custom proxies

import logging
from flask import Flask, Response
import custom_proxy.blueprint as bp
import webbrowser

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
url_prefix='/custom-proxy'

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.DEBUG)

app.register_blueprint(bp.app, url_prefix=url_prefix)


if __name__ == '__main__':
    webbrowser.open("http://localhost:5000"+url_prefix)
    app.run(debug=True)
