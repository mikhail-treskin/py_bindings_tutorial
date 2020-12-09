from setuptools import setup, Extension
from Cython.Build import cythonize
from sys import platform
import os

script_dir = os.path.dirname(__file__)
libs_dir = os.path.join(script_dir, "..", "..", "c_library", "build")
setup(
    name='cython demo',
    ext_modules=cythonize([
        Extension("extern_c_fibo", [os.path.join(script_dir, "extern_c", "c_fibo.pyx")],
                  libraries=[f"bindings_demo"],
                  library_dirs=[libs_dir]),
        Extension("pure_cython_fibo", [os.path.join(script_dir, "pure_cython", "cy_fibo.pyx")]),
    ]),
    zip_safe=False,
)
