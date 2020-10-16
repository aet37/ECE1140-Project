# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/src/HWTrackController/Main/include")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")

# Set source files (Unit tests)
set(HWTRACKCTRL_UNITTESTS
    HashMapUT.cpp
    HWTrackControllerRequestManagerUT.cpp
    ListUT.cpp
)

# Add executables (Suites)
add_executable(HWTrackCtrlTestSuite HWTrackCtrlTestSuite.cpp ${HWTRACKCTRL_UNITTESTS})
target_link_libraries(HWTrackCtrlTestSuite Catch2::Catch2 HWTrackController)
target_compile_definitions(HWTrackCtrlTestSuite PUBLIC BUILD_UNIT_TEST)

add_test(NAME HWTrackCtrlTestSuite COMMAND HWTrackCtrlTestSuite)