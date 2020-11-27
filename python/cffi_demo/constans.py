import os

script_dir = os.path.dirname(__file__)
# lib_path = os.path.join(script_dir, os.pardir, os.pardir, 'cmake-build-debug')
lib_path = "/Users/mikhailtreskin/repos/py_bindings_tutorial/c_library/cmake-build-debug/libbindings_demo.dylib"
include = os.path.join(script_dir, os.pardir, os.pardir, "c_library", "library.h")