# Find boost
find_package(Boost 1.53.0 COMPONENTS system)

# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Server")
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")
include_directories("${Boost_INCLUDE_DIRS}")

include_directories("${PROJECT_SOURCE_DIR}/include/SWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/TrainModel")

# CTC Module Includes
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")
include_directories("${PROJECT_SOURCE_DIR}/include/TrackModel")

# Add subdirectories
add_subdirectory(Debug)
add_subdirectory(CTC)
add_subdirectory(SWTrackController)
add_subdirectory(HWTrackController)
add_subdirectory(TrackModel)
add_subdirectory(TrainModel)
add_subdirectory(SWTrainController)
add_subdirectory(HWTrainController)

# Set source files
set(SOURCES
    Server/ConnectionHandler.cpp
    Server/Server.cpp
    Main.cpp
)

add_executable(main ${SOURCES})

target_link_libraries(main 
                      ${Boost_LIBRARIES}
                      CTC
                      SWTrackController
                      HWTrackController
                      TrackModel
                      TrainModel
                      SWTrainController
                      HWTrainController
                      debug_lib
)
