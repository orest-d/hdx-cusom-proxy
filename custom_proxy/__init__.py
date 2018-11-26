class ModuleNotFound(Exception):
    def __init__(self,repo,module):
        Exception.__init__("Module %(repo)s/%(module)s not found"%locals())

def get_code(repo, module):
    if repo == "builtin":
        if module == "test":
            return """
def hello(*arg):
    return "Hello, world"

def echo(repo, module, name, extension, request):
    return ",\\n".join((repo, module, name, extension))
"""    
    raise ModuleNotFound(repo,module)

def execute(code_text, repo, module, name, request):
    module_filename = "%(repo)s/%(module)s.py"%locals()
    code = compile(code_text, module_filename, "exec")

    elements = name.split(".")
    function = elements[0]
    if not all(ch.isalnum() or ch=="_" for ch in function):
        raise Exception("Wrong function name: "+function)

    extension = elements[1] if len(elements)>=2 else ""

    exec(code)
    f = eval(function)
    
    return f(repo, module, name, extension, request)

def do(repo, module, name, request):
    code_text = get_code(repo, module)
    return execute(code_text, repo, module, name, request)