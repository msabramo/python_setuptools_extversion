python_setuptools_extversion
============================

Adds an `extversion` param to `setup` that can specify various ways of
getting a version string dynamically, from an external source:

- A Python function
- An external program (e.g.: `git`, `hg`, etc.)

In particular, there are some shortcuts that make it really easy to
generate the version from the following sources:

- git tags
- hg (Mercurial) tags
- text file
- environment variable

git tags
--------

Generate version using git tags:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion='git',
)
```

This generates a version like `v23.0.2-develop-4-g79f3bc0-dirty`.

This version signifies that the tree was on the `develop` branch 4
commits after the `v23.0.2` tag. The hash is `79f3bc0` (the "g"
preceding the hash indicates git) and the working directory is dirty.

This version is generated by invoking `git describe --tags --dirty`.

hg (Mercurial tags)
-------------------

Generate version using hg tags:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion='hg',
)
```

This generates a version like
`6.1.1-strip-leading-non-digits-from-tags-2-m1ae06831e549`.

This version signifies that the tree was on the
`strip-leading-non-digits-from-tags` branch 2
commits after the `6.1.1` tag. The hash is `1ae06831e549` (the "m"
preceding the hash indicates Mercurial).

This version is generated by invoking `hg log -r . --template
'{latesttag}-{branch}-{latesttagdistance}-m{node|short}'`.

text file
---------

Read (slurp) the version from a file called `VERSION.txt`:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion=('slurp', ['VERSION.txt']),
)
```

The file is assumed to be in the same directory as `setup.py` - you do
not need to do the dance where you do stuff like:

```python
os.path.join(os.path.dirname(__file__), 'VERSION.txt')
```

Under the covers, the infrastructure temporarily changes the current
directory to the directory containing `setup.py` before executing.

environment variable
--------------------

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion=('getenv', ['PYTHON_PACKAGE_VERSION']),
)
```

custom via an external program
------------------------------

To indicate an external command that should be called, enclose it in
backquotes.

For example:

```python
setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion='`date +"%Y.%m.%d.%H.%M.%S"`',
)
```

custom via a Python function
----------------------------

You can set `extversion` to a Python callable (e.g.: function, bound
method, etc.):

```python
def get_version(distribution):
    return raw_input("Please enter a version string for %s: "
                     % distribution.metadata.name)

setup(
    name='my_distribution',
    setup_requires=['setuptools_extversion'],
    extversion=get_version,
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
