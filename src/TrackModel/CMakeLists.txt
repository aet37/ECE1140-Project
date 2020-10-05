# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/TrackModel")

# Set source files
set(SOURCES
    main.cpp
)

add_library(TrackModel STATIC ${SOURCES})
