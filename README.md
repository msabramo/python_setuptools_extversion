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
    setup_requires=['setuptools_extversion'],
    extversion=extversion,
)
```

Above, `extversion` is a callable (a plain function in this case) that
accepts one parameter with a `setuptools.dist.Distribution`. It's silly
of course to just return a static string here, as you could've just used
the `version` parameter of vanilla setuptools. But this illustrates the
basic concept and you can make your real-life function do something much
more interesting.

Instead of providing a `callable` object, you can provide a dotted-path
string to specify the function -- e.g.:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion='my_package.version:get_package_version',
)
```

There is no need to `import` the module; the `import` will be done for
you automatically, on-demand.

One thing that is useful to do is to call an external command -- you may
want to run, say, `git describe --tags --dirty` to generate your version
number. You could of course do this using the features already
described, by writing a Python function that invokes a subprocess. But
there is a shortcut that saves you from the trouble of doing this:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion={'command': 'git describe --tags --dirty'},
)
```

Note that this is quite flexible and powerful. You could set `command`
to:

- A command for another VCS such as Mercurial, bzr, etc.
- A shell script or Python program that does whatever:
  - Maybe fetch the version from a text file?
  - Maybe fetch the version from some database or server?
  - Maybe just a simple program that prompts for the version number on
    the console?
  (Have other ideas? Send me a PR!)

