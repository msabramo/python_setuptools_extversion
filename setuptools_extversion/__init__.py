"""
setuptools_extversion

Allows getting distribution version from external sources (e.g.: shell command,
Python function)
"""

import pkg_resources
import subprocess


VERSION_PROVIDER_KEY = 'extversion'


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
                extversion = function(value.get('function'))
        else:
            raise Exception('Unknown type for %s = %r' % (attr, value))
        dist.metadata.version = extversion(dist)


class command(object):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __call__(self, distribution):
        return subprocess.check_output(*self.args, **self.kwargs).strip()


class function(object):
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        if isinstance(self.func, basestring):
            ep = pkg_resources.EntryPoint.parse('x=' + self.func)
            self.func = ep.load(False)
            args = list(self.args + args)
            kwargs = dict(self.kwargs)
            kwargs.update(kwargs)
        return self.func(*args, **kwargs)
