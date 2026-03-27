cmake_minimum_required(VERSION 3.15)
project(libb CXX)

find_package(logger REQUIRED)

add_library(libb STATIC src/libB.cpp)
target_include_directories(libb PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)

target_link_libraries(libb PRIVATE logger::logger)

install(TARGETS libb DESTINATION lib)

# CRITICAL: This copies libb.h to the package 'include' folder
install(DIRECTORY inc/ DESTINATION include)
