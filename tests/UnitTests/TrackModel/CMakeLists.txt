# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/TrackModel")

# Set source files (Unit tests)
set(TRACKMODEL_UNITTESTS
    TrackModelUT.cpp
)

# Add executables (Suites)
add_executable(TrackModelTestSuite TrackModelTestSuite.cpp ${TRACKMODEL_UNITTESTS})
target_link_libraries(TrackModelTestSuite Catch2::Catch2 TrackModel)

add_test(NAME TrackModelTestSuite COMMAND TrackModelTestSuite)