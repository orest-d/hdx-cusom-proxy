from flask import Response, send_file
from werkzeug.exceptions import NotFound
import pandas as pd
from io import BytesIO
import os.path
import urllib.request
import urllib.error
import logging
import sys, imp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

MIMETYPES = dict(
    json="application/json",
    txt= 'text/plain',
    html= 'text/html',
    htm= 'text/html',
    md = 'text/markdown',
    xls = 'application/vnd.ms-excel',
    xlsx = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    ods = 'application/vnd.oasis.opendocument.spreadsheet',
    tsv='text/tab-separated-values',
    csv = 'text/csv',
    msgpack = 'application/x-msgpack',
    hdf5 = 'application/x-hdf',
    h5 = 'application/x-hdf'
)

TEXT_MIMETYPES = "json txt htm html md tsv csv".split()
LOCAL_PROXIES_PATH=os.path.join(os.path.split(os.path.split(__file__)[0])[0],"my-proxies")
OD_PROXIES_URL = "https://raw.githubusercontent.com/orest-d/hdx-custom-proxy/master/my-proxies/"

class ModuleNotFound(NotFound):
    def __init__(self,repo,module):
        NotFound.__init__(self, "Module %(repo)s/%(module)s not found"%locals())

class FunctionNotFound(NotFound):
    def __init__(self,repo,module, function):
        NotFound.__init__(self, "Function %(function)s not found in module %(repo)s/%(module)s"%locals())

def get_code(repo, module):
    if repo == "builtin":
        logger.info("Get builtin repo")
        if module == "test":
            logger.info("Get module test")
            return """
def hello(*arg):
    return "Hello, world"

def indirect_hello(*arg):
    return "Indirect "+hello()

def echo(repo, module, name, extension, request):
    return ",\\n".join((repo, module, name, extension, repr(request.args)))


def pandas_test(*arg):
    import pandas
    return pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))

def error(*arg):
    raise Exception("Test error")
"""
    if repo == "local":
        try:
            path = os.path.join(LOCAL_PROXIES_PATH,module+".py")
            logger.info("Get module "+path)
            return open(path).read()
        except FileNotFoundError:
            raise ModuleNotFound(repo, module)
    elif repo == "od":
        try:
            return urllib.request.urlopen(OD_PROXIES_URL+module+".py").read()
        except urllib.error.HTTPError:
            raise ModuleNotFound(repo, module)


    raise ModuleNotFound(repo, module)

def execute(code_text, repo, module, name, request):
    module_filename = "%(repo)s/%(module)s.py"%locals()
    code = compile(code_text, module_filename, "exec")

    elements = name.split(".")
    function = elements[0]
    if not all(ch.isalnum() or ch=="_" for ch in function):
        raise Exception("Wrong function name: "+function)

    extension = elements[1] if len(elements) >= 2 else ""

    pymodule = imp.new_module(module)
    exec(code, pymodule.__dict__)
    try:
        f = getattr(pymodule,function)
    except NameError:
        raise FunctionNotFound(repo, module, function)
    
    return f(repo, module, name, extension, request)

def do(repo, module, name, request):
    elements = name.split(".")
    function = elements[0]
    extension = elements[1] if len(elements)>=2 else ""
    code_text = get_code(repo, module)

    result = execute(code_text, repo, module, name, request)

    mimetype = MIMETYPES.get(extension,"text/plain")
    if isinstance(result,pd.DataFrame):
        df = result
        if extension == "csv":
            return Response(df.to_csv(index=False), mimetype=mimetype)
        if extension == "tsv":
            return Response(df.to_csv(index=False, sep="\t"), mimetype=mimetype)
        if extension == "json":
            return Response(df.to_json(index=False, orient="table"), mimetype=mimetype)
        if extension in ("html", "htm"):
            return Response(df.to_html(index=False), mimetype=mimetype)
        if extension == "xlsx":
            output = BytesIO()
            writer = pd.ExcelWriter(output, engine='xlsxwriter')
            df.to_excel(writer,function)
            writer.close()
            output.seek(0)
            return send_file(output, attachment_filename=name, as_attachment=True)
        if extension == "msgpack":
            output = BytesIO()
            df.to_msgpack(output)
            output.seek(0)
            return send_file(output, attachment_filename=name, as_attachment=True)
        return Response(df.to_csv(index=False), mimetype=mimetype)

    if isinstance(result,str):
        if extension in TEXT_MIMETYPES:
            return Response(result, mimetype=mimetype)

    return result