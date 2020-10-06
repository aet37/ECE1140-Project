# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrainController")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    main.cpp
)

add_library(HWTrainController STATIC ${SOURCES})
target_link_libraries(HWTrainController debug_lib)