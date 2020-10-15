# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrainController")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    SWTrainControllerMain.cpp
    ControlSystem.cpp
)

add_library(SWTrainController STATIC ${SOURCES})
target_link_libraries(SWTrainController debug_lib)
