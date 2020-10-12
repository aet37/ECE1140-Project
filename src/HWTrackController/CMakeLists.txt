# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    HWTrackControllerRequestManager.cpp
)

add_library(HWTrackController STATIC ${SOURCES})
target_link_libraries(HWTrackController debug_lib)
