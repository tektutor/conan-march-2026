cmake_minimum_required(VERSION 3.15)
project(ConanExample LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# 1. Find the library (CMakeDeps makes this work behind the scenes)
find_package(fmt REQUIRED)

# 2. Create your executable
add_executable(my_app main.cpp)

# 3. Link the library to your executable
target_link_libraries(my_app PRIVATE fmt::fmt)
