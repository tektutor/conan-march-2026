cmake_minimum_required(VERSION 3.30)

project(hello LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(hello_lib 1.0 REQUIRED)

add_executable(hello src/main.cpp)

target_link_libraries(hello PRIVATE hello_lib::hello_lib)
