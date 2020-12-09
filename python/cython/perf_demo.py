import sys
import os
from timeit import default_timer
from tabulate import tabulate
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'c_library', 'build'))

from python.cython.extern_c.extern_c_fibo import extern_c_fibo
from python.cython.extern_c.pure_cython_fibo import *

py_times = []
py_int_times = []
cy_cdef_times = []
cy_cpdef_times = []
extern_c_times = []
iters = 10
for i in range(iters):
    t0 = default_timer()
    fib(30)
    py_times.append(default_timer() - t0)

    t0 = default_timer()
    fib_int(30)
    py_int_times.append(default_timer() - t0)

    t0 = default_timer()
    fib_cdef(30)
    cy_cdef_times.append(default_timer() - t0)

    t0 = default_timer()
    fib_cpdef(30)
    cy_cpdef_times.append(default_timer() - t0)

    t0 = default_timer()
    extern_c_fibo(30)
    extern_c_times.append(default_timer() - t0)


py_mean = np.mean(py_times)
py_int_mean = np.mean(py_int_times)
cy_cdef_mean = np.mean(cy_cdef_times)
cy_cpdef_mean = np.mean(cy_cpdef_times)
extern_c_mean = np.mean(extern_c_times)

fastest_mean = np.min([py_mean, py_int_mean, cy_cdef_mean, cy_cpdef_mean, extern_c_mean])
headers = ["Library", "Mean", "Ratio"]
results = [
    ["Python", py_mean, fastest_mean / py_mean],
    ["Python with types", py_int_mean, fastest_mean / py_int_mean],
    ["Cython cdef", cy_cdef_mean, fastest_mean / cy_cdef_mean],
    ["Cython pdef", cy_cpdef_mean, fastest_mean / cy_cpdef_mean],
    ["Extern C", extern_c_mean, fastest_mean / extern_c_mean],
]
print(tabulate(results, headers=headers, tablefmt='fancy_grid'))