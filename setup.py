# run: python setup.py build_ext --inplace && python main.py

import Cython.Compiler.Options
from Cython.Distutils import build_ext
from setuptools import setup
from setuptools import Extension
from os.path import join
Cython.Compiler.Options.annotate = True

name = 'sandpiles'
files = [
    join('sandpiles', '__init__.pyx'),
]

ext_modules = [Extension(
    name,
    sources=files,
    language='c')
]

for mod in ext_modules:
    mod.cython_directives = {
        'language_level': 3,
        'boundscheck': False,
        'wraparound': False,
        'cdivision': True
    }

setup(
    name=name,
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext},
)
