def hello(*arg):
    return "Hello, world"


def echo(repo, module, name, extension, request):
    return ",\\n".join((repo, module, name, extension))


def pandas_test(*arg):
    import pandas
    return pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))
