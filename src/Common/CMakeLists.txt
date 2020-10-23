# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    DebugRequestManager.cpp
    RequestManagerRepository.cpp
)
set(CMAKE_CXX_STANDARD 17)

add_library(Common STATIC ${SOURCES})
target_link_libraries(Common debug_lib)
