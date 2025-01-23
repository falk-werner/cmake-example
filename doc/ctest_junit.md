# CTest JUnit XML

This document describes CTest's JUnit XML dialect.
Source can be found at [cmCTestTestHandler.cxx](https://github.com/Kitware/CMake/blob/master/Source/CTest/cmCTestTestHandler.cxx) (method WriteJUnitXML at line 2468 ff).

## Example

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuite name="Linux-c++"
	tests="4"
	failures="1"
	disabled="1"
	skipped="1"
	hostname="dev22"
	time="0"
	timestamp="2025-01-24T00:04:01"
	>
	<testcase name="plain.succeed" classname="plain.succeed" time="0.00161205" status="run">
		<properties>
			<property name="cmake_labels" value="Custom Label 1"/>
		</properties>
		<system-out>Running main() from ./googletest/src/gtest_main.cc
Note: Google Test filter = plain.succeed
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from plain
[ RUN      ] plain.succeed

[       OK ] plain.succeed (0 ms)
[----------] 1 test from plain (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 1 test.
</system-out>
	</testcase>
	<testcase name="plain.skipped" classname="plain.skipped" time="0.00147304" status="notrun">
		<skipped message="SKIP_REGULAR_EXPRESSION_MATCHED"/>
		<properties/>
		<system-out>Running main() from ./googletest/src/gtest_main.cc
Note: Google Test filter = plain.skipped
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from plain
[ RUN      ] plain.skipped
/home/user/src/ctest-example/test-src/test_plain.cpp:10: Skipped
skipped test
[  SKIPPED ] plain.skipped (0 ms)
[----------] 1 test from plain (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 0 tests.
[  SKIPPED ] 1 test, listed below:
[  SKIPPED ] plain.skipped
</system-out>
	</testcase>
	<testcase name="plain.fail" classname="plain.fail" time="0.00135954" status="fail">
		<failure message="Failed"/>
		<properties/>
		<system-out>Running main() from ./googletest/src/gtest_main.cc
Note: Google Test filter = plain.fail
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from plain
[ RUN      ] plain.fail
/home/user/src/ctest-example/test-src/test_plain.cpp:15: Failure
Failed
failed test
[  FAILED  ] plain.fail (0 ms)
[----------] 1 test from plain (0 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (0 ms total)
[  PASSED  ] 0 tests.
[  FAILED  ] 1 test, listed below:
[  FAILED  ] plain.fail

 1 FAILED TEST
</system-out>
	</testcase>
	<testcase name="plain.test" classname="plain.test" time="0" status="disabled">
		<properties/>
		<system-out>Disabled</system-out>
	</testcase>
</testsuite>
```

## Elements

| Name                      | Description   |
| ------------------------- | ------------- |
| [testsuite](#testsuite)   | Root element. |
| [testcase](#testcase)     | Test case. |
| [skipped](#skipped)       | Skipped message. |
| [failure](#failure)       | Failure message. |
| [properties](#properties) | Test case properties. |
| [property](#property)     | Single test case property. |
| [system-out](#system-out) | Test case output. |

## testsuite

Root Element.

### Attributes

| Name     | Type   | Description |
| -------- | ------ | ----------- |
| name     | string | [CTest Build name](https://cmake.org/cmake/help/latest/variable/CTEST_BUILD_NAME.html) |
| tests    | int    | Count of test cases. |
| failures | int    | Count of failed test cases. |
| disabled | int    | Count of disabled test cases. |
| skipped  | int    | Count of skipped test cases. |
| hostname | string | [CTest Site](https://cmake.org/cmake/help/latest/variable/CTEST_SITE.html) |
| time     | int | Duration of test execution in seconds. |
| timestamp | string | Timestamp of test execution in ISO8601 short format (YYYY-MM-DDThh:mm:ss) |

### Elements

| Name                  | Cardinality | Description |
| --------------------- | ----------- | ----------- |
| [testcase](#testcase) | 0..*        | Test case.  |

## testcase

Test Case.

### Attributes

| Name      | Type   | Description |
| --------- | ------ | ----------- |
| name      | string | Name of the test case (`cmCTestTestResult`). |
| classname | string | Same as `name`. |
| time      | float  | Execution time of the test case in seconds. |
| status    | enum   | Test status. One of `run`, `disabled`, `notrun` or `fail` |

### Elements

| Name                | Cardinality | Description |
| ------------------- | ----------- | ----------- |
| [skipped](#skipped) | 0..1        | Skipped message. Only present if `status` is `notrun`. |
| [failure](#failure) | 0..1        | Failure message. Only present if `status` is `fail`. |
| [properties](#properties) | 1     | Test case properties. |
| [system-out](#system-out) | 1     | Output of the test case. |


## skipped

Skipped message.

### Attributes

| Name    | Type   | Description |
| ------- | ------ | ----------- |
| message | string | Message.    | 

## failure

Failure message.

### Attributes

| Name    | Type   | Description |
| ------- | ------ | ----------- |
| message | string | Message.    | 

## properties

Properties of a test case.

### Elements

| Name                  | Cardinality | Description |
| --------------------- | ----------- | ----------- |
| [property](#property) | 0..*        | Single test case property. |

## property

Single test case property.

### Attributes

| Name  | Type   | Description |
| ----- | ------ | ----------- |
| name  | string | Name of the property. |
| value | string | Value of the property. |

### Known Properties

| Name | Description |
| ---- | ----------- |
| cmake_labels | List of [CTest Labels](https://cmake.org/cmake/help/latest/prop_test/LABELS.html) |

## system-out

Output of the test case. Content-only.
