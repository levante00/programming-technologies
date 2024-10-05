cmake_minimum_required(VERSION 2.8)

project(C)

set(CMAKE_CXX_STANDARD 11) 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/bin)


execute_process(
    COMMAND python3 preparing.py
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/A
    OUTPUT_VARIABLE "index.h"
			 
)
execute_process(
    COMMAND  mv index.h 
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/A/index.h
)

add_executable(
    ${PROJECT_NAME} 
    ${CMAKE_CURRENT_SOURCE_DIR}/C/main.cpp
)

add_executable(
    CTest
    ${CMAKE_CURRENT_SOURCE_DIR}/C/main_run.cpp
    ${CMAKE_CURRENT_SOURCE_DIR}/C/main_test.cpp
)

target_link_libraries(CTest Cgener_lib)

include_directories(
     ${CMAKE_CURRENT_SOURCE_DIR}
)

add_subdirectory (
    ${CMAKE_CURRENT_SOURCE_DIR}/B
)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/609281088cfefc76f9d0ce82e1ff6c30cc3591e5.zip
)

FetchContent_MakeAvailable(googletest)

enable_testing()

target_link_libraries(CTest gtest_main)
