import logging
from flask import Flask, Response, Blueprint, request, redirect, url_for
import custom_proxy as cp

app = Blueprint('hdxcp', __name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index.html', methods=['GET', 'POST'])
def index():
    return """
<html>
    <head>
        <title>HDX Custom Proxy</title>
    </head>
    <body>
        <h1>HDX Custom Proxy</h1>
        For more info, see the <a href="https://github.com/orest-d/hdx-custom-proxy">repository</a>.
        <h4>Test</h4>
        <ul>
           <li><a href="p/builtin/test">Builtin test</a></li>
           <li><a href="p/local/test">Local test</a></li>
        </ul>
    </body>    
</html>
"""

@app.route('/p/<string:repo>/<string:module>/<string:name>')
def serve(repo, module, name):
    return cp.do(repo, module, name, request)

@app.route('/p/<string:repo>/<string:module>')
def serve_index(repo, module):
    return redirect(url_for(".serve",repo=repo,module=module,name="index.html"))
