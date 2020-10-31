# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrainController")

# Set source files (Unit tests)
set(SWTRAINCONTROLLER_UNITTESTS
    SWTrainControllerUT.cpp
    ControllerUT.cpp
)

# Add executables (Suites)
add_executable(SWTrainControllerTestSuite SWTrainControllerTestSuite.cpp ${SWTRAINCONTROLLER_UNITTESTS})
target_link_libraries(SWTrainControllerTestSuite Catch2::Catch2 SWTrainController)

add_test(NAME SWTrainControllerTestSuite COMMAND SWTrainControllerTestSuite)