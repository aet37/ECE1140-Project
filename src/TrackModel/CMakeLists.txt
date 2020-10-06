# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/TrackModel")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    main.cpp
)

add_library(TrackModel STATIC ${SOURCES})
target_link_libraries(TrackModel debug)
