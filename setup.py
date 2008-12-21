r"""A MSAA client library.

"""
import sys, os
from distutils.core import setup, Command, DistutilsOptionError
import pyia

classifiers = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: LGPLv2.2',
    'Operating System :: Microsoft :: Windows',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
    ]

setup(name="pyia",
      description="Python MSAA client library",
      long_description = __doc__,
      author="Eitan Isaacson",
      author_email="eitan@ascender.com",
      url="http://github.com/eeejay/pyia/tree/master",
      download_url = "http://github.com/eeejay/pyia/tree/master",
      license="LGPLv2.2",
      classifiers=classifiers,
      version=pyia.__version__,
      packages=["pyia"])
