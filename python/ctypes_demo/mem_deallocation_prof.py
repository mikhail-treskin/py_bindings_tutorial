import ctypes
import numpy as np
import os
script_dir = os.path.dirname(__file__)
lib_path = os.path.join(script_dir, os.pardir, os.pardir, 'c_library', 'build', 'libbindings_demo.so')
lib = ctypes.CDLL(lib_path)

lib.gen_arr.restype = ctypes.POINTER(ctypes.c_int)
lib.gen_arr.argtypes = [ctypes.c_int, ]
arr_size = 1000000
data_p = lib.gen_arr(arr_size)

class ArrayWrap:
    def __init__(self, ptr, shape):
        self.array = np.ctypeslib.as_array(ptr, shape=shape)
        self.__lib_path = os.path.join(script_dir, os.pardir, os.pardir, 'c_library', 'build', 'libbindings_demo.so')
        self.__ptr = ptr
    def __del__(self):
        print("Python: object destructor invoked")
        lib = ctypes.CDLL(self.__lib_path)
        lib.free_arr.argtypes = [ctypes.POINTER(ctypes.c_int),]
        lib.free_arr(self.__ptr)

array_wrap = ArrayWrap(data_p, (arr_size, ))
print(f"Shaped numpy array:\n {array_wrap.array}")