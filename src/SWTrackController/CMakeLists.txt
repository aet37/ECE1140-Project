# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    SWTrackControllerMain.cpp
    TrackContoller.cpp
)
set(CMAKE_CXX_STANDARD 17)

add_library(SWTrackController STATIC ${SOURCES})
target_link_libraries(SWTrackController debug_lib)