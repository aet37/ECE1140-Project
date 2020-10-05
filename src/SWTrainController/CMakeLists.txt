# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/SWTrainController")

# Set source files
set(SOURCES
    main.cpp
)

add_library(SWTrainController STATIC ${SOURCES})
