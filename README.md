python_setuptools_extversion
============================

Adds an `extversion` param to setup that can be a callable

Examples
--------

This one is of dubious usefulness, but illustrates the very basic
concept.

```python
from setuptools import setup

def extversion(distribution):
    return '3.4.5'

setup(
    name='profilesvc',
    extversion=extversion,
)
```

Above, `extversion` is a callable (a plain function in this case) that
accepts one parameter with a `setuptools.Distribution`. It's silly of
course to just return a static string here, as you could've just used
the `version` parameter of vanilla setuptools. So on to a more useful
example...
