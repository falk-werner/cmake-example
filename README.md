# cmake-example

- [x] Execute Unit Tests
- [x] Execute Unit Tests using valgrind/memcheck
- [ ] Execute Unit Tests using valgrind/helgrind
- [x] Static Code Analysis using clang-tidy
- [x] Measure Code Coverage during test execution
- [X] Cross-Compile

## Coverage

```
lcov -c -d . -o coverage.info
genhtml main_coverage.info --output-directory out
```
