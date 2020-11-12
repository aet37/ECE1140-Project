# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrainController")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    HWTrainControllerMain.cpp
    HWTrainRequestManager.cpp
)
set(CMAKE_CXX_STANDARD 17)

add_library(HWTrainController STATIC ${SOURCES})
target_link_libraries(HWTrainController debug_lib SWTrainController)