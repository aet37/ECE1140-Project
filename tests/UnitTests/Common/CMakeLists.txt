# Set include directories
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/TrackModel")
include_directories("${PROJECT_SOURCE_DIR}/include/TrainModel")
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrainController")
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrainController")

# Set source files (Unit tests)
set(COMMON_UNITTESTS
    RequestManagerRepositoryUT.cpp
    RequestUT.cpp
    ServiceQueueUT.cpp
)

set(CMAKE_CXX_STANDARD 17)

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
                      SWTrainController
)

add_test(NAME CommonTestSuite COMMAND CommonTestSuite)