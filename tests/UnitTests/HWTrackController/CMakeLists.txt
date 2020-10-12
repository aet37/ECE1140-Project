# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")

# Set source files (Unit tests)
set(HWTRACKCTRL_UNITTESTS
    HWTrackControllerRequestManagerUT.cpp
)

# Add executables (Suites)
add_executable(HWTrackCtrlTestSuite HWTrackCtrlTestSuite.cpp ${HWTRACKCTRL_UNITTESTS})
target_link_libraries(HWTrackCtrlTestSuite Catch2::Catch2 HWTrackController)

add_test(NAME HWTrackCtrlTestSuite COMMAND HWTrackCtrlTestSuite)