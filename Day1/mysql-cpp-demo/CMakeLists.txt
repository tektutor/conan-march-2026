cmake_minimum_required(VERSION 3.10)

project(mysql-cpp-demo)

set(CMAKE_CXX_STANDARD 17)

find_package(MYSQL REQUIRED)

add_executable(mysql-cpp-demo src/main.cpp)

target_include_directories(mysql-cpp-demo PRIVATE ${MYSQL_INCLUDE_DIRS})

target_link_libraries( mysql-cpp-demo
	mysqlcppconn
)
