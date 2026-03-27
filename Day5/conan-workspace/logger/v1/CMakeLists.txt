cmake_minimum_required(VERSION 3.15)
project(logger VERSION 1.0 LANGUAGES CXX)

add_library(logger src/logger.cpp)

target_include_directories(logger PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/inc)

# CRITICAL: This copies liblogger.a to the package 'lib' folder
install(TARGETS logger DESTINATION lib)

# CRITICAL: This copies logger.h to the package 'include' folder
install(DIRECTORY inc/ DESTINATION include)
