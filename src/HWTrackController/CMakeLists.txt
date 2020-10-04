# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")

# Set source files
set(SOURCES
    RequestManager.cpp
)

add_library(HWTrackController STATIC ${SOURCES})
