cmake_minimum_required(VERSION 3.15)
project(app CXX)

find_package(liba REQUIRED)
find_package(libb REQUIRED)

add_executable(app src/main.cpp)
# We link against A and B, which both now point to logger 2.0
target_link_libraries(app liba::liba libb::libb)
