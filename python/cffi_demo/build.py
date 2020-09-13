import os
import cffi


ffi = cffi.FFI()
# Путь расположение скрипта
PATH = os.getcwd()

script_dir = os.path.dirname(__file__)
lib_path = os.path.join(script_dir, os.pardir, os.pardir, 'cmake-build-debug')
include = os.path.join(script_dir, os.pardir, os.pardir, "c_library", "library.h")

# test.h заголовочный файл нашей библиотеки
# указываем путь до него относительно build.py
with open(include) as f:
    ffi.cdef(f.read())

ffi.set_source("_test", # имя библиотеки собранной cffi, добавляем префикс _
               # Подключаем test.h, указываем путь относительно собираемой _test
               f'#include "{include}"',
               # Где находится libtest.so (Исходная собранная библиотека)
               # относительно _test.cpython-36m-x86_64-linux-gnu.so (создается CFFI)
               libraries=[lib_path, "./bindings_demo"],
               library_dirs=[PATH, 'objs/'],
               )

# компилируем _test в папку lib
ffi.compile(tmpdir='./lib')