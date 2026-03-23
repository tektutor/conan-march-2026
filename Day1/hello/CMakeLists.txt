cmake_minimum_required(VERSION 3.16)

project(hello LANGUAGES CXX) 

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

add_executable(hello src/main.cpp src/hello.cpp)

target_include_directories(hello PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/inc)
