def index(*arg):
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
               <li><a href="hello.txt">Hello</a></li>
               <li><a href="indirect_hello.txt">Indirect Hello</a></li>
               <li><a href="echo.txt">Echo</a></li>             
               <li>Pandas test
                 <a href="pandas_test.csv">(csv)</a>
                 <a href="pandas_test.tsv">(tsv)</a>
                 <a href="pandas_test.html">(html)</a>
                 <a href="pandas_test.json">(json)</a>
                 <a href="pandas_test.msgpack">(msgpack)</a>
                 <a href="pandas_test.xlsx">(xlsx)</a>
               </li>
               <li><a href="error.txt">Error</a></li>             
               <li>HXL test
                 <a href="hxl_test.csv?url=https%3A//data.humdata.org/dataset/98574e10-6866-4f13-a2b1-3c8312801af5/resource/c78846cc-2989-49b5-8dd8-d7364ecdd35d/download/wfp_food_median_prices_yemen.csv">(csv)</a>
                 <a href="hxl_test.html?url=https%3A//data.humdata.org/dataset/98574e10-6866-4f13-a2b1-3c8312801af5/resource/c78846cc-2989-49b5-8dd8-d7364ecdd35d/download/wfp_food_median_prices_yemen.csv">(html)</a>
               </li>
             </ul>
           </li>
        </ul>
    </body>    
</html>
"""

def hello(*arg):
    return "Hello, world"

def indirect_hello(*arg):
    return "Indirect "+hello()

def echo(repo, module, name, extension, request):
    return ",\n".join((repo, module, name, extension, repr(request.args)))

def pandas_test(*arg):
    import pandas as pd
    return pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))

def error(*arg):
    raise Exception("Test error")

def hxl_test(repo, module, name, extension, request):
    import hxl
    return hxl.data(request.args["url"])
    