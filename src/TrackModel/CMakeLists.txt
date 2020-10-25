# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/TrackModel")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    TrackModelMain.cpp
)
set(CMAKE_CXX_STANDARD 17)

add_library(TrackModel STATIC ${SOURCES})
target_link_libraries(TrackModel debug_lib TrainModel)
