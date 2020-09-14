cmake_minimum_required(VERSION 3.16)
project(bindings_demo C)

set(CMAKE_C_STANDARD 99)

add_library(bindings_demo SHARED basic_funcs.c library.h arrays.c vars.c)