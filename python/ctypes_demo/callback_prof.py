import ctypes
import numpy as np
import os
import platform
if platform == "darwin":
    ext = "dylib"
else:
    ext = "so"
script_dir = os.path.dirname(__file__)
lib_path = os.path.join(script_dir, os.pardir, os.pardir, 'c_library', 'build', f'libbindings_demo.{ext}')
lib = ctypes.CDLL(lib_path)

arr = np.ones(shape=(50000000), dtype=np.int32)

arr_p = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
func_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
lib.upd_arr.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_uint, func_type]

@func_type
def py_func(a):
    return a

lib.upd_arr(arr_p, arr.size, py_func)