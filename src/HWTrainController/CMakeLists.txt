# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrainController")

# Set source files
set(SOURCES
    main.cpp
)

add_library(HWTrainController STATIC ${SOURCES})
