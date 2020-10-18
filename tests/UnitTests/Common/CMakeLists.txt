# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")

# Set source files (Unit tests)
set(COMMON_UNITTESTS
    RequestManagerRepositoryUT.cpp
    ServiceQueueUT.cpp
)

# Add executables (Suites)
add_executable(CommonTestSuite CommonTestSuite.cpp ${COMMON_UNITTESTS})
target_link_libraries(CommonTestSuite 
                      Catch2::Catch2 
                      ${CMAKE_THREAD_LIBS_INIT} 
                      Common 
                      HWTrackController 
                      CTC
                      TrainModel
                      TrackModel
                      HWTrainController
                      SWTrackController
                      SWTrainController)

add_test(NAME CommonTestSuite COMMAND CommonTestSuite)