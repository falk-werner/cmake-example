cmake_minimum_required (VERSION 3.22)
project(foo)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -g -fprofile-arcs -ftest-coverage")
link_libraries(debug gcov)

set(CMAKE_CXX_CLANG_TIDY clang-tidy -checks=-*,modernize-*,readability-*)

add_library(foo STATIC src/foo.cpp)
target_include_directories(foo PUBLIC include)

enable_testing()
include(CTest)
find_package(GTest REQUIRED)
include(GoogleTest)
add_executable(foo_test test-src/foo_test.cpp)
set_target_properties(foo_test PROPERTIES CXX_CLANG_TIDY "")
target_link_libraries(foo_test PRIVATE foo GTest::gtest GTest::gtest_main)
gtest_discover_tests(foo_test EXTRA_ARGS "--gtest_output=xml:test-results.xml")

