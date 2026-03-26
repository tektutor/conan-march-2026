cmake_minimum_required(VERSION 3.30)

project(myQtApp LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

find_package(Qt6 REQUIRED COMPONENTS Widgets WaylandClient)

add_executable(myQtApp
	main.cpp
	MyDlg.cpp
	MyDlg.h
)

target_link_libraries(myQtApp PRIVATE Qt6::Widgets Qt6::WaylandClient)
