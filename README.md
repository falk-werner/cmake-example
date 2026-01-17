# cmake-example

This repository contains an example `cmake` project to demonstrate some build-in features of [cmake](https://cmake.org/).

- [x] generate pkg-config file
- [x] unit tests using [googletest](https://github.com/google/googletest)
- [x] static code analysis using [clang-tidy](https://clang.llvm.org/extra/clang-tidy/)
- [x] dynamic code analysis using [valgrind/memcheck](https://valgrind.org/)
- [x] measure code coverage using [gcov](https://gcc.gnu.org/onlinedocs/gcc/Gcov.html)
- [X] cross-compilation and use of [qemu](https://www.qemu.org/)

## Basic Usage

Please use the [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) provided by this project since it contains all tool needed by the example also including
a cross compiler and a suitable cmake toolchain file.

Since this is an ordinary `cmake` project, it can be compiled using the following commands:

```bash
cmake -DCMAKE_BUILD_TYPE=Debug -B build
cmake --build build
```

To execute unit tests, `ctest` can be used:

```bash
ctest --test-dir build
```

The project itself is nothing special, it provided a static C++ library called `libfoo` and
a basic unit test for that library. The project is organized as follows:

| Directory | Decription |
| --------- | ---------- |
| include   | contains public headers of `libfoo` |
| src       | contains implementation of `libfoo` |
| test-src  | constains unit tests of `libfoo` |

Note that code coverage is only available in debug configuration.

## Provide pkg-config file

Libraries should provide a `pkg-config` (`.pc`) file describing their compiler settings and dependencies.
This way, projects depending on the library can use `pkg-config` to setup include paths, library paths and compiler flags.

Using `cmake`, the `pkg-config` can be generated using project settings.
See [cmake documentation](https://cmake.org/cmake/help/latest/command/configure_file.html) for further information.

```cmake
configure_file(foo.pc.in foo.pc @ONLY) 
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/foo.pc
    DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
```

## Unit Tests

To support unit tests, `cmake` comes with the `ctest` tool, which can be used to run an executable as unit test. Since `googletest` is a popular
unit test framework for C/C++ projects, `cmake` comes with a built-in
support for `googletest`.

```cmake
enable_testing()
include(CTest)

find_package(GTest REQUIRED)
include(GoogleTest)

add_executable(foo_test test-src/foo_test.cpp)

target_link_libraries(foo_test PRIVATE foo GTest::gtest GTest::gtest_main)
gtest_discover_tests(foo_test)
```

With this preparation, `ctest` is invoked as follows:  
_(Note that the project must be build before.)_

```bash
ctest --test-dir build
```

### Generating Junit-XML

For test reports, [JUnit XML](https://www.ibm.com/docs/de/developer-for-zos/14.1?topic=formats-junit-xml-format) is a standard format that is supported by a wide variety of tools.

To generate `JUnit XML` during unit tests, there are 2 easy options provided by `cmake`:

- using `googletest`
- using `ctest`

To make `googletest` create `JUnit XML` the `--gtest_output` option is used:

```cmake
gtest_discover_tests(foo_test EXTRA_ARGS "--gtest_output=xml:test-results.xml")
```

The other option is to use `ctest`:

```bash
ctest --output-junit test-report.xml --test-dir build
```

### Other ctest options

Note that `ctest` comes with a rich variety of options.
Take a look at the [ctest documentation](https://cmake.org/cmake/help/latest/manual/ctest.1.html) to learn about them.

Some, like code coverage and dynamic code analysis will be described below. But most options were not described here, e.g. specifying test timeouts.

Also note that most command line options can also be specified in
`CMakeLists.txt`.

## Static Code Analysis

To enable static code analysis using `clang-tidy` the only thing to do is
to specify the desired checks in `CMakeLists.txt`:

```cmake
set(CMAKE_CXX_CLANG_TIDY clang-tidy -checks=-*,modernize-*,readability-*)
```

This will enable `clang tidy` for each target. Since one might not wish
to check each target (e.g. unit tests), `clang-tidy` can also be deactivated
per target:

```cmake
set_target_properties(foo_test PROPERTIES CXX_CLANG_TIDY "")
```

## Dynamic Code Analysis

Dynamic code analysis is supported by `cmake` using `ctest`.
To run the specified unit tests using `memcheck`, the following command line is used:

```bash
ctest -T memcheck --test-dir build
```

Note that `ctest` can be further configured using `CMakeList.txt` to
use other valgrind tools and / or to tweak valgrind options, e.g. to
use suppression files.

## Code Coverage

Code coverage is also integrated in `ctest`. To enable coverage
generation, compile options and link options must be set in
`CMakeLists.txt`:

```cmake
target_compile_options(foo PUBLIC -coverage)
target_link_options(foo PUBLIC -coverage)
```

After that, the test must be executed and coverage can be obtained.
```bash
ctest --test-dir build
ctest -T coverage --test-dir build
```

This comamnd will print the current coverage on command line.


To generate an `HTML` view of the coverage, `lcov` can be used:

```bash
# collect coverage information and store them in to coverage.info
lcov -c -d . -o coverage.info --rc lcov_branch_coverage=1 --ignore-errors mismatch

# remove coverage information of standard and system libraries
lcov -r coverage.info "/usr*" -o coverage.info --rc lcov_branch_coverage=1

# remove coverage information of test sources
lcov -r coverage.info "test-src/*" -o coverage.info --rc lcov_branch_coverage=1

# generate HTML report in out directory
genhtml coverage.info --output-directory out --rc genhtml_branch_coverage=1
```

## Cross-Compilation

To support cross compilation, `cmake` has the concept of `toolchain` files.
Here is an example of such a file:

```cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)

set(CMAKE_C_COMPILER /usr/bin/arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER /usr/bin/arm-linux-gnueabihf-g++)
set(CMAKE_C_COMPILER_WORKS 1)
set(CMAKE_CXX_COMPILER_WORKS 1)

set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

set(CMAKE_CROSSCOMPILING_EMULATOR qemu-arm.sh)
```

Within a toolchain file all toolchain specific tools and settings can be specified.
To cross compile, the toolchain file must be specified during initial `cmake` setup:

```bash
cmake --toolchain=cmake/toolchain/arm.cmake -DCMAKE_BUILD_TYPE=Debug -B build
```

_(Make sure to clear the build directory before this command, otherwise you might
get an error.)_

Cross-compiling using `cmake` has a good integration with `qemu`. Please notice the
variable `CMAKE_CROSSCOMPILING_EMULATOR` in the toolchain file above. This variable
defines an executable that is used to invoke platform specific binaries.

Thanks to this, execution of unit tests and and obtaining code coverage can be
done using `ctest` as described above.  
_(Note that `valgrind` will not work this way.)_
