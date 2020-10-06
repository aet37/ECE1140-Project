# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/CTC")
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    main.cpp
)

add_library(CTC STATIC ${SOURCES})
target_link_libraries(CTC debug_lib)
