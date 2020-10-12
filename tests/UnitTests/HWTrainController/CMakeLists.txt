# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrainController")

# Set source files (Unit tests)
set(HWTRAINCONTROLLER_UNITTESTS
    HWTrainControllerUT.cpp
)

# Add executables (Suites)
add_executable(HWTrainControllerTestSuite HWTrainControllerTestSuite.cpp ${HWTRAINCONTROLLER_UNITTESTS})
target_link_libraries(HWTrainControllerTestSuite Catch2::Catch2 HWTrainController)

add_test(NAME HWTrainControllerTestSuite COMMAND HWTrainControllerTestSuite)