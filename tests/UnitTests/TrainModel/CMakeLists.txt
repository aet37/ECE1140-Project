# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/TrainModel")

# Set source files (Unit tests)
set(TRAINMODEL_UNITTESTS
    TrainModelUT.cpp
)

# Add executables (Suites)
add_executable(TrainModelTestSuite TrainModelTestSuite.cpp ${TRAINMODEL_UNITTESTS})
target_link_libraries(TrainModelTestSuite Catch2::Catch2 TrainModel)

add_test(NAME TrainModelTestSuite COMMAND TrainModelTestSuite)