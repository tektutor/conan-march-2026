cmake_minimum_required(VERSION 3.16)

project(hello LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(lib)

add_executable(hello src/main.cpp)

target_link_libraries(hello PRIVATE hello_lib)
