# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrackController")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")
include_directories("${PROJECT_SOURCE_DIR}/src/Server")

# Set source files
set(SOURCES
    CTCMain.cpp
    CTCRequestManager.cpp
    TrainSystem.cpp
)
set(CMAKE_CXX_STANDARD 17)

add_library(CTC STATIC ${SOURCES})
target_link_libraries(CTC SWTrackController debug_lib)
