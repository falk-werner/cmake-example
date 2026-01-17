#!/bin/bash

set -x
set -e

rm -f coverage.info
rm -rf out

cmake -B build -D CMAKE_BUILD_TYPE=Debug -D WITH_COVERAGE=ON -D WITHOUT_TIFY=ON
cmake --build build
ctest --test-dir build
ctest -T coverage --test-dir build
lcov -c -d . -o coverage.info --rc lcov_branch_coverage=1 --ignore-errors mismatch
lcov -r coverage.info "/usr*" -o coverage.info --rc lcov_branch_coverage=1
lcov -r coverage.info "test-src/*" -o coverage.info --rc lcov_branch_coverage=1
genhtml coverage.info --output-directory out --rc genhtml_branch_coverage=1
