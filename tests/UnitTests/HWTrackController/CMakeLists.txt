# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/src/HWTrackController/Main/include")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files (Unit tests)
set(HWTRACKCTRL_UNITTESTS
    HashMapUT.cpp
    HWTrackControllerRequestManagerUT.cpp
    ListUT.cpp
)
set(CMAKE_CXX_STANDARD 17)

# Add executables (Suites)
add_executable(HWTrackCtrlTestSuite HWTrackCtrlTestSuite.cpp ${HWTRACKCTRL_UNITTESTS})
target_link_libraries(HWTrackCtrlTestSuite Catch2::Catch2 HWTrackController)
target_compile_definitions(HWTrackCtrlTestSuite PUBLIC BUILD_UNIT_TEST)

add_test(NAME HWTrackCtrlTestSuite COMMAND HWTrackCtrlTestSuite)