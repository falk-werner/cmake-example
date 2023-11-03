cmake_minimum_required (VERSION 3.22)
project(foo 
    VERSION 1.0.0
    DESCRIPTION "some static library"
    HOMEPAGE_URL https://github.com/falk-werner/cmake-example/)

option(WITHOUT_TEST "Disable unit test" OFF)

# Default C++ options
set(CMAKE_CXX_STANDARD 17)

# Enable code coverage (debug configuration only)
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -g -fprofile-arcs -ftest-coverage")
link_libraries(debug gcov)

# Activate clang tidy for all targets by default
set(CMAKE_CXX_CLANG_TIDY clang-tidy -checks=-*,modernize-*,readability-*)

# libfoo: static library, single header, .pc-file
add_library(foo STATIC src/foo.cpp)
target_include_directories(foo PUBLIC include)
set_target_properties(foo PROPERTIES PUBLIC_HEADER include/foo.hpp)
install(TARGETS foo)

configure_file(foo.pc.in foo.pc @ONLY) 
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/foo.pc
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)


# Do not depend on any unit test stuff when they are not active
if(NOT(WITHOUT_TEST))

enable_testing()
include(CTest)

find_package(GTest REQUIRED)
include(GoogleTest)

add_executable(foo_test test-src/foo_test.cpp)

# disable clang-tidy for unit test executables
set_target_properties(foo_test PROPERTIES CXX_CLANG_TIDY "")

target_link_libraries(foo_test PRIVATE foo GTest::gtest GTest::gtest_main)
gtest_discover_tests(foo_test EXTRA_ARGS "--gtest_output=xml:test-results.xml")

endif()
