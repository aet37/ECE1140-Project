# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Common")
include_directories("${PROJECT_SOURCE_DIR}/include/TrainModel")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    main.cpp
)

add_library(TrainModel STATIC ${SOURCES})
target_link_libraries(TrainModel debug_lib)
