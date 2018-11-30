def hxl_test(repo, module, name, extension, request):
    """Example of a proxy returning hxl Dataset and fetching the data from a link passed by url argumet.
    Automatic type conversion works for Dataset.
    """
    import hxl
    return hxl.data(request.args["url"])
