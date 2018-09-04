# Travis CI directory

## Run all the tests!

When developing on your platform at home, you should be able to run the tests
from either a Windows, Linux, or Mac machine by simply running `$pytest`. That
should give you something that looks like this.

```
=============================================================================== test session starts ================================================================================
platform linux2 -- Python 2.7.15rc1, pytest-3.7.3, py-1.6.0, pluggy-0.7.1
rootdir: /home/bleehu/3_cx_docs/CXDocs/travis, inifile:
collected 1 item                                                                                                                                                                   

test_start.py .                                                                                                                                                              [100%]

============================================================================= 1 passed in 0.13 seconds =============================================================================
```

## Writing tests

When writing tests, make sure to put them in this directory and name them 
something to the effect of `test_*.py` so that pytest will find them during its
collection phase.

When writing tests in python, use the `assert` keyword. Alternatively, you could
use `exit(0)` for a successful test or another number to indicate failure. 

## Documentation

Most of our testing follows the conventions from these documents. 
1. The [Flask Testing Tutorial](http://flask.pocoo.org/docs/1.0/testing/)
2. The [Travis CI Documentation](https://docs.travis-ci.com/user/languages/python/)