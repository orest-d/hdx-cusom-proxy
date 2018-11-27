import logging
from flask import Flask, Response, Blueprint, request
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
           <li>Builtin test
             <ul>
               <li><a href="p/builtin/test/hello.txt">Hello</a></li>
               <li><a href="p/builtin/test/indirect_hello.txt">Indirect Hello</a></li>
               <li><a href="p/builtin/test/echo.txt">Echo</a></li>             
               <li>Pandas test
                 <a href="p/builtin/test/pandas_test.csv">(csv)</a>
                 <a href="p/builtin/test/pandas_test.tsv">(tsv)</a>
                 <a href="p/builtin/test/pandas_test.html">(html)</a>
                 <a href="p/builtin/test/pandas_test.json">(json)</a>
                 <a href="p/builtin/test/pandas_test.msgpack">(msgpack)</a>
                 <a href="p/builtin/test/pandas_test.xlsx">(xlsx)</a>
               </li>
               <li><a href="p/builtin/test/error.txt">Error</a></li>             
             </ul>
           </li>
        </ul>
    </body>    
</html>
"""

@app.route('/p/<string:repo>/<string:module>/<string:name>')
def serve(repo, module, name):
    return cp.do(repo, module, name, request)

@app.route('/p/<string:repo>/<string:module>')
def serve_index(repo, module):
    return cp.do(repo, module, "index.html", request)
