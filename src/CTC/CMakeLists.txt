# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")

# Set source files
set(SOURCES
    main.cpp
)

add_library(CTC STATIC ${SOURCES})
