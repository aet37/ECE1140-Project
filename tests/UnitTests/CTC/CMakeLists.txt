# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")

# Set source files (Unit tests)
set(COMMON_UNITTESTS
    CTCDefUT.cpp
)

# Add executables (Suites)
add_executable(CTCTestSuite CTCTestSuite.cpp ${COMMON_UNITTESTS})
target_link_libraries(CTCTestSuite Catch2::Catch2 Common CTC)

add_test(NAME CommonTestSuite COMMAND CommonTestSuite)