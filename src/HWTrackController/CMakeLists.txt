# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")

# Set source files
set(SOURCES
    RequestManager.cpp
)

add_library(HWTrackController STATIC ${SOURCES})
