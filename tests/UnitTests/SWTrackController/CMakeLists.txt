# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrackController")

# Set source files (Unit tests)
set(SWTRACKCONTROLLER_UNITTESTS
    SWTrackControllerUT.cpp
)

# Add executables (Suites)
add_executable(SWTrackControllerTestSuite SWTrackControllerTestSuite.cpp ${CTC_UNITTESTS})
target_link_libraries(SWTrackControllerTestSuite Catch2::Catch2 SWTrackController)

add_test(NAME SWTrackControllerTestSuite COMMAND SWTrackControllerTestSuite)