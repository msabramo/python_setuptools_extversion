"""
setuptools_extversion

Allows getting distribution version from external sources (e.g.: shell command,
Python function)
"""

import contextlib
import os
import pkg_resources
import subprocess
import sys


# True if we are running on Python 3.
PY3 = sys.version_info[0] == 3

if PY3: # pragma: no cover
    string_types = str,
else:
    string_types = basestring,


VERSION_PROVIDER_KEY = 'extversion'


def git(distribution):
    cmd = command(['git', 'describe', '--tags', '--dirty'])
    return cmd(distribution)


def hg(distribution):
    cmd = command([
        'hg', 'log', '-r .',
        '--template',
        '{latesttag}-{branch}-{latesttagdistance}-m{node|short}'])
    return cmd(distribution)


def read_file(filename, distribution):
    return open(filename).read().strip()


def version_calc(dist, attr, value):
    """
    Handler for parameter to setup(extversion=value)
    """

    if attr == VERSION_PROVIDER_KEY:
        if callable(value):
            extversion = value
        elif hasattr(value, 'get'):
            if value.get('command'):
                extversion = command(value.get('command'), shell=True)
            if value.get('function'):
                extversion = function(
                    value.get('function'),
                    *value.get('args', ()),
                    **value.get('kwargs', {}))
        elif isinstance(value, string_types):
            if value.startswith('`'):
                cmd = value[1:-1]
                extversion = command(cmd, shell=True)
            else:
                extversion = function(value)
        else:
            raise Exception('Unknown type for %s = %r' % (attr, value))

        setup_py_dir = os.path.dirname(sys.argv[0])

        with chdir(setup_py_dir):
            dist.metadata.version = extversion(distribution=dist)


@contextlib.contextmanager
def chdir(new_dir):
    if new_dir:
        old_dir = os.curdir
        os.chdir(new_dir)
    yield
    if new_dir:
        os.chdir(old_dir)


class command(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, distribution):
        return subprocess.check_output(*self.args, **self.kwargs).strip()


class PkgResourcesResolver(object):
    parse = pkg_resources.EntryPoint.parse

    def maybe_resolve(self, dotted):
        if isinstance(dotted, basestring):
            entry_point = self.parse('x=' + dotted)
            return entry_point.load(False)

        return dotted


class function(object):
    default_resolver = PkgResourcesResolver()

    def __init__(self, func, resolver=None, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.resolver = resolver or self.default_resolver

    def __call__(self, *args, **kwargs):
        self.func = self.resolver.maybe_resolve(self.func)
        args = list(self.args + args)
        kwargs = dict(self.kwargs.items() + kwargs.items())
        return self.func(*args, **kwargs)
