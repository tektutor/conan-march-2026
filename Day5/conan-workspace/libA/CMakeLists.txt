cmake_minimum_required(VERSION 3.15)
project(liba CXX)

find_package(logger REQUIRED)

add_library(liba STATIC src/libA.cpp)
target_include_directories(liba PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)

target_link_libraries(liba PRIVATE logger::logger)

install(TARGETS liba DESTINATION lib)

# CRITICAL: This copies libb.h to the package 'include' folder
install(DIRECTORY inc/ DESTINATION include)
