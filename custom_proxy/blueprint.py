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
    </body>    
</html>
"""

@app.route('/p/<string:repo>/<string:module>/<string:name>')
def serve(repo, module, name):
    return cp.do(repo, module, name, request)


@app.route('/api/original_data.csv')
def original_data_csv():
    return Response(ecbfx.csv_content(), mimetype="text/csv")

@app.route('/api/data_with_hxl.csv')
def data_with_hxl_csv():
    df = ecbfx.add_hxl_tags(ecbfx.df_content())
    return Response(df.to_csv(index=False), mimetype="text/csv")

@app.route('/api/fx/fx_rates_in_<string:currency>.csv')
def rates_in_currency_csv(currency):
    df = ecbfx.df_content()
    df = ecbfx.add_base_currency(df)
    df = ecbfx.convert_currency(df,currency)
    df = ecbfx.add_hxl_tags(df)
    return Response(df.to_csv(index=False), mimetype="text/csv")
