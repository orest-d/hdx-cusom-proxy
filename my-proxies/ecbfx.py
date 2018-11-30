import logging
from urllib.request import urlopen
import zipfile
import os.path
import io
import pandas as pd


def data_url():
    return "https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.zip"

def index(*arg):
    return """
<html>
    <head>
        <title>HDX ECB reference FX</title>
    </head>
    <body>
        <h1>HDX interface to <a href="https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html">ECB reference FX rates</a></h1>
        Data source: %s

        <ul>
            <li><a href="original_data.zip">Original data (zip)</a></li>
            <li><a href="original_data.csv">Original data (csv)</a></li>
            <li><a href="original_data.xlsx">Original data (xlsx)</a></li>
            <li><a href="data_with_hxl.csv">Data with HXL tags (csv)</a></li>
            <li><a href="fx_rates.csv">FX rates in USD (csv)</a></li>
        </ul>
    </body>
</html>
""" % data_url()

def original_data(repo, module, name, extension, request):
    """Proxy returning original data fetched directly from data_url()
    Unzipping and format conversion is supported via custom_proxy.
    """
    if extension=="zip":
        return raw_data()
    else:
        return df_content()

def data_with_hxl(*arg):
    """Data fetched from data_url() enhanced with hxl tags."""
    return add_hxl_tags(df_content())

def fx_rates(repo, module, name, extension, request):
    """Proxy returning original data fetched directly from data_url()"""
    currency = request.args.get("currency","USD")
    df = df_content()
    df = add_base_currency(df)
    df = convert_currency(df, currency)
    df = add_hxl_tags(df)
    return df

def raw_data(url=None):
    url = data_url() if url is None else url
    return urlopen(url).read()

def csv_content(url=None):
    "Fetch the raw csv data"
    zipdata = raw_data(url)
    zf = zipfile.ZipFile(io.BytesIO(zipdata),"r")
    name = [n for n in zf.namelist() if os.path.splitext(n)[1].lower()==".csv"][0]
    return zf.read(name)

def df_content(url=None,add_base_currency=False,base_currency="EUR"):
    "Fetch the data as a dataframe"
    return pd.read_csv(io.BytesIO(csv_content(url)))

def add_base_currency(df,base_currency="EUR"):
    df.loc[:,base_currency]=1.0
    return df

def convert_currency(df, to_currency="USD", base_currency="EUR"):
    currency_columns = [c for c in df.columns if c.lower()!="date"]
    scale = (df.loc[:,base_currency]/df.loc[:,to_currency]).values.copy()
    for c in currency_columns:
        df.loc[:,c]*=scale
    return df

def add_hxl_tags(df):
    hxl = [("#date" if c.lower()=="date" else "#value +"+str(c))for c in df.columns]
    hxl_df = pd.DataFrame([hxl],columns=df.columns)
    df = hxl_df.append(df)
    return df

