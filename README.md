# hdx-custom-proxy
Custom reverse proxy for HDX data

This module provides a simple way to define custom proxies in cases when more complex preprocessing is necessary than
what can be achieved by hxl proxy (see https://proxy.hxlstandard.org/data/source).

Custom proxy allows to execute reverse proxies defined as python scripts stored on web (e.g. in github).
Custom proxy functionality is implemented as a flask blueprint and it can be tested by executing _service.py_.

Proxies are organized in a following way:
* _Repository_ is typically a place on internet containing python files. Repository is identified by a repository name, the mapping between repository names and urls is hardcoded in LINK dictionary in ```/custom_proxy/__init__.py``` (e.g. _od_ links to a _my-proxies_ folder of the _proxies_ branch of this repository). In order to define new repositories, the LINKS need to be set up. Besides repositories defined by LINKS, two more repositories are defined:
  * _builtin_ - is defined inside the custom_proxy module containing a single module _test_. This can be used for testing the functionality of the custom_proxy.
  * _local_ - gets the modules from a local filesystem from the my-proxies directory.
* _Module_ is a python file (with .py extension) containing proxies. Module name is the file name without the extension.
* _Proxy_ is a python function inside the module. Proxy is called with 5 arguments: repo, module, name, extension, request.
  * _repo_ - repository name
  * _module_ - module name
  * _name_ - file name in the url request sent to the proxy function, including the extension. File name is composed from the function name and file extension separated by a dot.
  * _extension_ - file extension of the requested file name. 
  * _request_ - flask request object - useful for extracting e.g. url parameters.

Proxy function always needs to accept 5 parameters, but it may ignore them.
The simplest proxy can be written as:
```python
def hello(*arg):
    return "Hello, world"
```
Proxy function will be accessible from an url with the following structure:
http://domain.name/blueprint_prefix/p/repo/module/function_name.ext?optional_arguments,
e.g. http://localhost:5000/custom-proxy/p/builtin/test/hello.txt
Omitting function_name.ext will invoke index.html, i.e. an index function and extension html.

Proxy may return any valid flask response, e.g. a string or Response object.
On top of that proxy may return a pandas DataFrame object or hxl.Dataset from python-libhxl library. (Further objects may be supported in the future.)
In such a case custom_proxy automatically performs a format conversion to one of the currently supported formats: csv, tsv, xlsx, json, msgpack and html and it as well fills in the correct mime-type.
In a case not covered by supported types, proxy function is expected to perform the necessary format conversion based on the file extension (passed as an argument).

Further examples of proxies:

```python
# Accept explicitly all the proxy arguments and echo them together with the url parameters
# obtained from a request.
def echo(repo, module, name, extension, request):
    return ",\n".join((repo, module, name, extension, repr(request.args)))

# Return a data frame, which will be automatically converted to the desired format.
# Try to call as e.g. pandas_test.csv, pandas_test.html or with any other supported format.
def pandas_test(*arg):
    import pandas as pd
    return pd.DataFrame(dict(a=[1, 2, 3], b=[4, 5, 6]))

# Return a hxl Dataset fetched from an url passed as a parameter in the url request
# e.g. hxl_test.csv?url=https%3A//data.humdata.org/dataset/98574e10-6866-4f13-a2b1-3c8312801af5/resource/c78846cc-2989-49b5-8dd8-d7364ecdd35d/download/wfp_food_median_prices_yemen.csv
# Conversion to a proper format is done automatically.
def hxl_test(repo, module, name, extension, request):
    import hxl
    return hxl.data(request.args["url"])
```
