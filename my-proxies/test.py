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