cmake_minimum_required(VERSION 2.8)

project(Cgener)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_library(
     ${PROJECT_NAME}_lib SHARED
     ${CMAKE_CURRENT_SOURCE_DIR}/lib.cpp
)

target_include_directories(
    ${PROJECT_NAME}_lib
    PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)
