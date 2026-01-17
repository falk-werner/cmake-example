cmake_minimum_required (VERSION 3.22)
project(foo 
    VERSION 1.0.0
    DESCRIPTION "some static library"
    HOMEPAGE_URL https://github.com/falk-werner/cmake-example/)

option(WITHOUT_TEST "Disable unit test" OFF)
option(WITH_COVERAGE "Enable coverage" OFF)
option(WITHOUT_TIDY "Disable clang tidy" OFF)

# Default C++ options
set(CMAKE_CXX_STANDARD 17)

# Activate clang tidy for all targets by default
if(NOT(WITHOUT_TIDY))
set(CMAKE_CXX_CLANG_TIDY clang-tidy -checks=-*,modernize-*,readability-*)
endif()

# libfoo: static library, single header, .pc-file
add_library(foo STATIC src/foo.cpp)
target_include_directories(foo PUBLIC include)
set_target_properties(foo PROPERTIES PUBLIC_HEADER include/foo.hpp)
install(TARGETS foo)

configure_file(foo.pc.in foo.pc @ONLY) 
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/foo.pc
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)

# Enable code coverage 
if(WITH_COVERAGE)
target_compile_options(foo PUBLIC -coverage)
target_link_options(foo PUBLIC -coverage)
endif()


# Do not depend on any unit test stuff when they are not active
if(NOT(WITHOUT_TEST))

enable_testing()
include(CTest)

find_package(GTest REQUIRED)
include(GoogleTest)

add_executable(alltests test-src/foo_test.cpp)

# disable clang-tidy for unit test executables
set_target_properties(alltests PROPERTIES CXX_CLANG_TIDY "")

target_link_libraries(alltests PRIVATE foo GTest::gtest GTest::gtest_main)
gtest_discover_tests(alltests EXTRA_ARGS "--gtest_output=xml:test-results.xml")

endif()
