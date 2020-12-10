# Cython

Cython is a programming language that aims to be a superset of the Python programming language, designed to give C-like performance with code that is written mostly in Python with optional additional C-inspired syntax.

Cython gives you the combined power of Python and C to let you:

* write Python code that calls back and forth from and to C or C++ code natively at any point.
* easily tune readable Python code into plain C performance by adding static type declarations, also in Python syntax.
* use combined source code level debugging to find bugs in your Python, Cython and C code.
* interact efficiently with large data sets, e.g. using multi-dimensional NumPy arrays.
quickly build your * applications within the large, mature and widely used CPython ecosystem.
* integrate natively with existing code and data from legacy, low-level or high-performance libraries and applications.

## Building Cython code
Cython code must, unlike Python, be compiled. This happens in two stages:

* A .pyx file is compiled by Cython to a .c file, containing the code of a Python extension module.
* The .c file is compiled by a C compiler to a .so file (or .pyd on Windows) which can be import-ed directly into a Python session. setuptools takes care of this part. Although Cython can call them for you in certain cases.

## Building with setuptools

Imagine a simple “hello world” script in a file hello.pyx:
```python
def say_hello_to(name):
    print("Hello %s!" % name)
```
The following could be a corresponding setup.py script:
```python
from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize("hello.pyx"),
    zip_safe=False,
)
```
## Building with CMake

To build the project with cmake you should have in cmake folder next files: ```FindCython.cmake```, ```UseCython.cmake```.
```cmake
# Defines the CMake commands/policies
cmake_minimum_required( VERSION 2.8.5 )

# Set the project name
project( CYTHON_CMAKE_EXAMPLE )

# Make the scripts available in the 'cmake' directory available for the
# 'include()' command, 'find_package()' command.
set( CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} ${CMAKE_CURRENT_LIST_DIR}/cmake )

# Include the CMake script UseCython.cmake.  This defines add_cython_module().
# Instruction for use can be found at the top of cmake/UseCython.cmake.
include( UseCython )

# Create target
cython_add_module(${TARGET_NAME} ${SOURCE})

```
[Link](https://github.com/thewtex/cython-cmake-example) to the example.

## Example
Let's imagine we have ```Rectangle.hpp``` file with Rectangle class:
```cpp
namespace shapes {
    class Rectangle {
        public:
            int x0, y0, x1, y1;
            Rectangle();
            Rectangle(int x0, int y0, int x1, int y1);
            ~Rectangle();
            int getArea();
            void getSize(int* width, int* height);
            void move(int dx, int dy);
    };
}
```
We now need to declare the attributes and methods for use on Cython. We put those declarations in a file called ```Rectangle.pxd```. 
```python
cdef extern from "Rectangle.hpp" namespace "shapes":
    cdef cppclass Rectangle:
        Rectangle() except +
        Rectangle(int, int, int, int) except +
        int x0, y0, x1, y1
        int getArea()
        void getSize(int* width, int* height)
        void move(int, int)
```
Note that the constructor is declared as “except +”. If the C++ code or the initial memory allocation raises an exception due to a failure, this will let Cython safely raise an appropriate Python exception instead. Without this declaration, C++ exceptions originating from the constructor will not be handled by Cython.

```Rectangle.pyx```

```python
from Rectangle cimport Rectangle

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class PyRectangle:
    cdef Rectangle c_rect  # Hold a C++ instance which we're wrapping

    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.c_rect = Rectangle(x0, y0, x1, y1)

    def get_area(self):
        return self.c_rect.getArea()

    def get_size(self):
        cdef int width, height
        self.c_rect.getSize(&width, &height)
        return width, height

    def move(self, dx, dy):
        self.c_rect.move(dx, dy)
    
    # Attribute access
    @property
    def x0(self):
        return self.c_rect.x0
    @x0.setter
    def x0(self, x0):
        self.c_rect.x0 = x0
```

## Standart library
Most of the containers of the C++ Standard Library have been declared in pxd files located in /```Cython/Includes/libcpp```. These containers are: deque, list, map, pair, queue, set, stack, vector.

```python
# distutils: language = c++

from libcpp.vector cimport vector

def main():
    cdef vector[int] v = [4, 6, 5, 10, 3]

    cdef int value
    for value in v:
        print(value)

    return [x*x for x in v if x % 2 == 0]
```

## One function - different implementations

```python
# pure python function
def fib(n):
    if n < 2:
        return n
    return fib(n-2) + fib(n-1)

def fib_cdef(int n):
    return fib_in_c(n)

cdef int fib_in_c(int n):
    if n < 2:
        return n
    return fib_in_c(n-2) + fib_in_c(n-1)

cpdef fib_cpdef(int n):
    if n < 2:
        return n
    return fib_cpdef(n-2) + fib_cpdef(n-1)
```

# pybind11
pybind11 is a lightweight header-only library that exposes C++ types in Python and vice versa, mainly to create Python bindings of existing C++ code. 
## Building with setuptools

To use pybind11 inside your setup.py, you have to have some system to ensure that pybind11 is installed when you build your package. There are four possible ways to do this, and pybind11 supports all four: You can ask all users to install pybind11 beforehand (bad), you can use PEP 518 requirements (Pip 10+ required) (good, but very new and requires Pip 10), Classic setup_requires (discouraged by Python packagers now that PEP 518 is available, but it still works everywhere), or you can Copy manually (always works but you have to manually sync your copy to get updates).

An example of a setup.py using pybind11’s helpers:
```python
from glob import glob
from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_modules = [
    Pybind11Extension(
        "python_example",
        sorted(glob("src/*.cpp")),  # Sort source files for reproducibility
    ),
]

setup(
    ...,
    ext_modules=ext_modules
)

```
An example project: [python_example](https://github.com/pybind/python_example).
 

## Building with CMake

For C++ codebases that have an existing CMake-based build system, a Python extension module can be created with just a few lines of code:
```cmake
cmake_minimum_required(VERSION 3.4...3.18)
project(example LANGUAGES CXX)

add_subdirectory(pybind11)
pybind11_add_module(example example.cpp)
```
This assumes that the pybind11 repository is located in a subdirectory named pybind11 and that the code is located in a file named example.cpp. The CMake command add_subdirectory will import the pybind11 project which provides the pybind11_add_module function. It will take care of all the details needed to build a Python extension module on any platform.

A working sample project, including a way to invoke CMake from setup.py for PyPI integration, can be found in the [cmake_example](https://github.com/pybind/cmake_example) repository.

More options of building Python API are described on the [website](https://pybind11.readthedocs.io/en/stable/compiling.html#).

## Basic example

The first two lines are always should be presented in your code. 
```cpp
#include <pybind11/pybind11.h>

namespace py = pybind11;

int add(int i, int j) {
    return i + j;
}

PYBIND11_MODULE(example, m) {
    m.doc() = "pybind11 example plugin"; // optional module docstring

    m.def("add", &add, "A function which adds two numbers");
}
```

The PYBIND11_MODULE() macro creates a function that will be called when an import statement is issued from within Python. The module name (example) is given as the first macro argument (it should not be in quotes). The second argument (m) defines a variable of type py::module_ which is the main interface for creating bindings. The method module_::def() generates binding code that exposes the add() function to Python.

```python
import example

example.add(1, 2)
```

### Keyword and default arguments

With a simple code modification, it is possible to inform Python about the names of the arguments (“i” and “j” in this case).
Unfortunately, pybind11 cannot automatically extract values of these parameters, since they are not part of the function’s type information. However, they are simple to specify using an extension of arg:

```cpp
int add(int i = 1, int j = 2) {
    return i + j;
}

PYBIND11_MODULE(example, m) {
    m.def("add", &add, "A function which adds two numbers", py::arg("i") = 1, py::arg("j") = 2);
}
```
The shorthand notation
```cpp
using namespace pybind11::literals;
m.def("add2", &add, "i"_a=1, "j"_a=2);
```

## Object-oriented code
```cpp
#include <pybind11/pybind11.h>

namespace py = pybind11;

struct Pet {
    Pet(const std::string &name) : name(name) { }
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }

    std::string name;
};

PYBIND11_MODULE(example, m) {
    py::class_<Pet>(m, "Pet")
        .def(py::init<const std::string &>())
        .def("setName", &Pet::setName)
        .def("getName", &Pet::getName);
}
```
class_ creates bindings for a C++ class or struct-style data structure. init() is a convenience function that takes the types of a constructor’s parameters as template arguments and wraps the corresponding constructor.
```python
>>> import example
>>> p = example.Pet('Molly')
>>> print(p)
<example.Pet object at 0x10cd98060>
>>> p.getName()
u'Molly'
>>> p.setName('Charly')
>>> p.getName()
u'Charly'
```
Static member functions can be bound in the same way using class_::def_static()
```cpp
py::class_<Pet>(m, "Pet")
    .def(py::init<const std::string &>())
    .def("setName", &Pet::setName)
    .def("getName", &Pet::getName)
    .def("__repr__",
        [](const Pet &a) {
            return "<example.Pet named '" + a.name + "'>";
        }
    );
```
```python
>>> print(p)
<example.Pet named 'Molly'>
```
Now suppose that Pet::name was a private internal variable that can only be accessed via setters and getters.
```cpp
class Pet {
public:
    Pet(const std::string &name) : name(name) { }
    void setName(const std::string &name_) { name = name_; }
    const std::string &getName() const { return name; }
private:
    std::string name;
};
```
In this case, the method `class_::def_property()` (`class_::def_property_readonly()` for read-only data) can be used to provide a field-like interface within Python that will transparently call the setter and getter functions:
```cpp
py::class_<Pet>(m, "Pet")
    .def(py::init<const std::string &>())
    .def_property("name", &Pet::getName, &Pet::setName)
```

## Smart pointers
### std::shared_pointer


The binding generator for classes, class_, can be passed a template type that denotes a special holder type that is used to manage references to the object. If no such holder type template argument is given, the default for a type named Type is ```std::unique_ptr<Type>```, which means that the object is deallocated when Python’s reference count goes to zero.
```cpp
class Child { };

class Parent {
public:
   Parent() : child(std::make_shared<Child>()) { }
   std::shared_ptr<Child> get_child() { return child.get(); }
private:
    std::shared_ptr<Child> child;
};

PYBIND11_MODULE(example, m) {
    py::class_<Child, std::shared_ptr<Child>>(m, "Child");

    py::class_<Parent, std::shared_ptr<Parent>>(m, "Parent")
       .def(py::init<>())
       .def("get_child", &Parent::get_child);
}
```
## STL containers
It's need to include `pybind11/stl.h` in order to convert from std::map<>, std::set<>, std::vector<>... to dict, set, list.

The major downside of these implicit conversions is that containers must be converted (i.e. copied) on every Python->C++ and C++->Python transition, which can have implications on the program semantics and performance.

[Link](https://pybind11.readthedocs.io/en/stable/index.html) to the documentation.


## Compare Cython vs pybind11 

Pybind11:

```c++
#include <pybind11/pybind11.h>

int fib(int n) {
    if (n < 2) {
        return n;
    }
    return fib(n-2) + fib(n-1);
}

namespace py = pybind11;

PYBIND11_MODULE(cmake_example, m) {

    m.def("fib", &fib, R"pbdoc(
        Count fibonacchi
    )pbdoc");
}
```
Cython:
```python
def fib_cdef(int n):
    return fib_in_c(n)

cdef int fib_in_c(int n):
    if n < 2:
        return n
    return fib_in_c(n-2) + fib_in_c(n-1)
```
Run python:
```python
from timeit import default_timer
import numpy as np

import cmake_example as cm
from  pure_cython_fibo import *

cy_times = []
py_times=[]
fib_val = 35

for i in range(100):
	t0 = default_timer()	
	cm.fib(fib_val)
	py_times.append(default_timer()-t0)
	t1 = default_timer()
	fib_cdef(fib_val)
	cy_times.append(default_timer()-t1)

print("cython: ", np.mean(cy_times))
print("pybind11: ", np.mean(py_times))
```
cython:  0.02642891739611514

pybind11:  0.02022730341530405


## Conclusion
### Cython
* Cython is good for speeding up chunks of Python code;
* It takes too long to create a python binding for an existing large library because there is a lot of additional code to write;
*  The entry point is quite high - you need to write code in cython (a mixture of C and Python).
### Pybind11
* Pybind11 was created specifically for C++11 (supports various C ++ functions), you write C ++ code;
* The entry point is lower;
* Has limitations with constants.
