#!/usr/bin/env python
from distutils.core import setup
from distutils.extension import Extension
import re
import numpy as np


def get_cython_version():
    """
    Returns:
        Version as a pair of ints (major, minor)

    Raises:
        ImportError: Can't load cython or find version
    """
    try:
        from Cython.Compiler.Version import version
        match = re.search(r'^([0-9]+)\.([0-9]+)', version)
        return [int(g) for g in match.groups()]
    except (ImportError, AttributeError):
        raise ImportError("Cython not found or version not compatible")


# Only use Cython if it is available, else just use the pre-generated files
try:
    cython_version = get_cython_version()
    # Requires Cython version 0.13 and up
    if cython_version[0] == 0 and cython_version[1] < 13:
        raise ImportError("Cython version too old")
    from Cython.Distutils import build_ext
    source_ext = '.pyx'
    cmdclass = {'build_ext': build_ext}
except ImportError:
    source_ext = '.c'
    cmdclass = {}


ext_modules = [Extension("freenect", ["freenect" + source_ext],
                         libraries=['usb-1.0', 'freenect', 'freenect_sync'],
                         runtime_library_dirs=['/usr/local/lib',
                                               '/usr/local/lib64',
                                               '/usr/lib/'],
                         extra_compile_args=['-fPIC', '-I', '../../include/',
                                             '-I', '/usr/include/libusb-1.0/',
                                             '-I', '/usr/local/include/libusb-1.0',
                                             '-I', '/usr/local/include',
                                             '-I', '../c_sync/',
                                             '-I', np.get_include()])]
setup(name='freenect',
      cmdclass=cmdclass,
      ext_modules=ext_modules)
