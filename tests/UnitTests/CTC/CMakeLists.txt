# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")

# Set source files (Unit tests)
set(CTC_UNITTESTS
        CTCDefUT.cpp
        CTCTrainSystemUT.cpp
)

# Add executables (Suites)
add_executable(CTCTestSuite CTCTestSuite.cpp ${CTC_UNITTESTS})
target_link_libraries(CTCTestSuite Catch2::Catch2 CTC)

add_test(NAME CTCTestSuite COMMAND CTCTestSuite)