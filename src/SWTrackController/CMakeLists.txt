# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    main.cpp
    TrackContoller.cpp
)

add_library(SWTrackController STATIC ${SOURCES})
target_link_libraries(SWTrackController debug_lib)