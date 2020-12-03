import ctypes
from ctypes.util import find_library
import numpy as np
import os
import random
from timeit import default_timer
# Loading library
script_dir = os.path.dirname(__file__)
lib_path = os.path.join(script_dir, os.pardir, os.pardir, 'c_library', 'build', 'libbindings_demo.dylib')
lib = ctypes.CDLL(lib_path)

##
# Manipulating with functions
##
print("=" * 100)
print("Manipulating with functions:\n")
lib.func_ret_int.restype = ctypes.c_int
lib.func_ret_int.argtypes = [ctypes.c_int, ]

lib.func_ret_double.restype = ctypes.c_double
lib.func_ret_double.argtypes = [ctypes.c_double]

lib.func_ret_str.restype = ctypes.c_char_p
lib.func_ret_str.argtypes = [ctypes.c_char_p, ]

lib.func_many_args.restype = ctypes.c_char
lib.func_many_args.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char, ctypes.c_short]

print('From Python Script: func_ret_int: ', lib.func_ret_int(101))
print('From Python Script: func_ret_double: ', lib.func_ret_double(12.123456789))
print('From Python Script: func_ret_str: ', lib.func_ret_str('Hello!'.encode('utf-8')).decode("utf-8"))
print('From Python Script: func_many_args: ',
      lib.func_many_args(15, 18.1617, 'X'.encode('utf-8'), 32000).decode("utf-8"))

print()

##
# Manipulating with variables
##
print("=" * 100)
print("Manipulating with variables:\n")

a = ctypes.c_int.in_dll(lib, "a")
print('From Python Script: a: ', a.value)
b = ctypes.c_double.in_dll(lib, "b")
print('From Python Script: b: ', b.value)
c = ctypes.c_char.in_dll(lib, "c")
print('From Python Script: c: ', c.value.decode("utf-8"))

# Assigning new value
a.value = 22
a = ctypes.c_int.in_dll(lib, "a")
print('From Python Script: a: ', a.value)
print()

##
# Working with arrays
##
print("=" * 100)
print("Manipulating with arrays:\n")
# Pointer from numpy ndarray
arr = np.asarray([[1, 2, 3], [4, 5, 6], [7, 8, 9]], dtype=np.int32)
data_p = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
arr_size = arr.size
el_size = arr.itemsize
dtype = str(arr.dtype).encode('utf-8')

lib.arr_minus_one.restype = None
lib.arr_minus_one.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
print(f"Python numpy array:\n {arr}")
lib.arr_minus_one(data_p, arr_size)
print(f"Python numpy array:\n {arr}")

# Pointer from python list
arr = [1, 2, 3, 4, 5, 6, 7, 8, 9]
data_p = (ctypes.c_int * len(arr))(*arr)
arr_size = 9
el_size = 4
dtype = "int32".encode("utf-8")
lib.arr_minus_one(data_p, arr_size, el_size, dtype)
print(f"Python list:\n {arr}")

# numpy array from pointer
lib.gen_arr.restype = ctypes.POINTER(ctypes.c_int)
lib.gen_arr.argtypes = [ctypes.c_int,]
array_size = 20
data_p = lib.gen_arr(array_size)

# Create from ctypes array
ctypes_arr = (ctypes.c_int * array_size).from_address(ctypes.addressof(data_p.contents))
flat_arr = np.ctypeslib.as_array(ctypes_arr, shape=(4, 5))  # Shape ignored
print(f"Flat numpy array:\n {flat_arr}")
# Create from pointer directly
shaped_array = np.ctypeslib.as_array(data_p, shape=(4, 5))
print(f"Shaped numpy array:\n {shaped_array}")

lib.fill_arr.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_uint]
lib.fill_arr.restype = None

# Pre-allocated data
i_arr = (ctypes.c_int * 15)()
i_p = ctypes.cast(i_arr, ctypes.POINTER(ctypes.c_int))
lib.fill_arr(i_p, 15)
# Build numpy array
shaped_array = np.ctypeslib.as_array(i_p, shape=(3, 5))
print(f"Shaped numpy array:\n {shaped_array}")

# Write directly to array's memory
arr = np.ndarray(shape=(5, 5), dtype=np.int32)
arr_p = arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
lib.fill_arr(arr_p, 25)
print(f"Shaped numpy array:\n {arr}")

# libc and find_library
libc = ctypes.CDLL(find_library('c'))

a = (ctypes.c_int * 10)(5, 1, 7, 33, 99, 43, 12, 5, 1, 0)
libc.qsort.restype = None

# callbacks functions
func_prototype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))


def py_cmp_func(a, b):
    return a[0] - b[0]


cmp_func = func_prototype(py_cmp_func)

libc.qsort(a, len(a), ctypes.sizeof(ctypes.c_int), cmp_func)
print([v for v in a])


def py_qsort(nums):
    if len(nums) <= 1:
        return nums
    else:
        q = random.choice(nums)
    l_nums = [n for n in nums if n < q]

    e_nums = [q] * nums.count(q)
    b_nums = [n for n in nums if n > q]
    return py_qsort(l_nums) + e_nums + py_qsort(b_nums)


# perf test
rand_arr = np.random.randint(low=0, high=500000, size=1000000, dtype=np.int32)

rand_list = list(rand_arr)
t0 = default_timer()
sorted_arr = py_qsort(rand_list)
t1 = default_timer()
print(f"Python qsort time: {t1 - t0}")
print(f"Sorted list slice {sorted_arr[0:100]}")

rand_data_p = rand_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
t0 = default_timer()
libc.qsort(rand_data_p, rand_arr.size, ctypes.sizeof(ctypes.c_int), cmp_func)
t1 = default_timer()
print(f"libc qsort with callback py time: {t1 - t0}")
print(f"Sorted array slice {rand_arr[0:100]}")

rand_arr = np.random.randint(low=0, high=500000, size=1000000, dtype=np.int32)
rand_data_p = rand_arr.ctypes.data_as(ctypes.POINTER(ctypes.c_int))
lib.qsort_wrap.restype = None
t0 = default_timer()
lib.qsort_wrap(rand_data_p, rand_arr.size, ctypes.sizeof(ctypes.c_int))
t1 = default_timer()
print(f"libc qsort wrap without py callback time: {t1 - t0}")
print(f"Sorted array slice {rand_arr[0:100]}")