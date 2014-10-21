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
    name='my_distribution',
    setup_requires='setuptools_extversion',
    extversion=extversion,
)
```

Above, `extversion` is a callable (a plain function in this case) that
accepts one parameter with a `setuptools.dist.Distribution`. It's silly
of course to just return a static string here, as you could've just used
the `version` parameter of vanilla setuptools. So on to a more useful
example...

A more useful thing to do is to generate the version from VCS tags --
here's an example for git -- here we run an external shell command:

```python
setup(
    name='my_distribution',
    setup_requires='setuptools_extversion',
    extversion={'command': 'git describe --tags --dirty'},
)
```

Note that this is quite flexible and powerful. You could set `command`
to:

- A command for another VCS such as Mercurial, bzr, etc.
- A shell script or Python program that does something custom.

If you prefer to do everything in Python and don't want to call a
subprocess, you could define a Python function to call by adding a
`'function'` key to the dict -- e.g.:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion={'function': 'my_package.version:get_package_version'},
)
```

This will call the specified function with a single argument which is
the `setuptools.dist.Distribution` object. Note that the value here can
be the callable itself or it can be a string containing a dotted path to
said function.

As a shortcut, you can simply provide the function directly as a string
or callable object and omit the dict:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion='my_package.version:get_package_version',
)
```

