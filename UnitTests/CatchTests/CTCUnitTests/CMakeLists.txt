cmake_minimum_required(VERSION 3.10)

project(CTCUnitTests)

# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/..")
include_directories("${PROJECT_SOURCE_DIR}/../../../include/CTC")

# Set source files
set(SOURCES
	CTCDef_test.cpp
)

# create unittests
add_executable(CTCUnitTests ${SOURCES})

enable_testing()

# unit tests
add_test(unittest CTCDef-tests)


