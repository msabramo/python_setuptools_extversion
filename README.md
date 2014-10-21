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
