# Find catch2
find_package(Catch2 REQUIRED)

# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/Server")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")

# Set source files (Unit tests)
set(SERVER_UNITTESTS
    ConnectionHandlerUT.cpp
)

# Add executables (Suites)
add_executable(ServerTestSuite ServerTestSuite.cpp ${SERVER_UNITTESTS})
target_link_libraries(ServerTestSuite Catch2::Catch2)