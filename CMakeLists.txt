cmake_minimum_required(VERSION 3.16)
project(bindings_demo C)

set(CMAKE_C_STANDARD 99)

add_library(bindings_demo SHARED c_library/basic_funcs.c c_library/library.h c_library/arrays.c c_library/vars.c)