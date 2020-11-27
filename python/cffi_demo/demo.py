import cffi
from timeit import default_timer
import os

from python.cffi_demo.constans import lib_path, include

"""In-Line ABI Mode"""
print("=" * 100)
print("In-Line ABI Mode Demo:\n")
ffi = cffi.FFI()

with open(include) as f:
    ffi.cdef(f.read())

t0 = default_timer()
lib = ffi.dlopen(lib_path)
t1 = default_timer()
print(f"In-line ABI import time {t1 - t0}")

res = lib.func_ret_str("Some str".encode("utf-8"))
print(f"From Python Script: {ffi.string(res).decode('utf-8')}")

"""Out-of-Line ABI Mode"""
print("=" * 100)
print("Out-of-Line ABI Mode Demo:\n")
try:
    from python.cffi_demo.out_of_line_abi._bindings_demo import ffi as out_of_line_abi_ffi
except ImportError:  # compile module if not found
    if "cffi" in globals():
        globals().pop("cffi")
    if "ffi" in globals():
        globals().pop("ffi")
    import cffi
    ffi = cffi.FFI()
    with open(include) as f:
        ffi.cdef(f.read())

    ffi.set_source("out_of_line_abi._bindings_demo", None)
    ffi.compile()

t0 = default_timer()
my_ffi_lib = out_of_line_abi_ffi.dlopen(lib_path)
t1 = default_timer()
print(f"Out-of-line ABI import time {t1 - t0}")
res = my_ffi_lib.func_ret_str("Some str".encode("utf-8"))
print(f"From Python Script: {ffi.string(res).decode('utf-8')}")

"""Out-of-Line API Mode"""
print("=" * 100)
print("Out-of-Line ABI Mode Demo:\n")
try:
    from python.cffi_demo.out_of_line_api._bindings_demo import ffi as out_of_line_api_ffi
    from python.cffi_demo.out_of_line_api._bindings_demo import lib as out_of_line_api_lib
except ImportError:  # compile module if not found
    if "cffi" in globals():
        globals().pop("cffi")
    if "ffi" in globals():
        globals().pop("ffi")
    import cffi
    ffi = cffi.FFI()
    with open(include) as f:
        ffi.cdef(f.read())
    ffi.set_source("_bindings_demo",  # имя библиотеки собранной cffi, добавляем префикс _
                   # Подключаем test.h, указываем путь относительно собираемой _test
                   '#include "../../c_library/library.h"',
                   # Где находится libtest.so (Исходная собранная библиотека)
                   # относительно _test.cpython-36m-x86_64-linux-gnu.so (создается CFFI)
                   libraries=["bindings_demo"],
                   library_dirs=[os.path.dirname(lib_path)],
                   )
    ffi.compile(tmpdir='./out_of_line_api')

# dlopen not required
res = out_of_line_api_lib.func_ret_str("Some str".encode("utf-8"))
print(f"From Python Script: {ffi.string(res).decode('utf-8')}")
