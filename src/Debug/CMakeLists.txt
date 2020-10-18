# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Debug")

# Set source files
set(SOURCES
    Assert.cpp
    DebugUtil.cpp
    Logger.cpp
)
set(CMAKE_CXX_STANDARD 17)

# Make library
add_library(debug_lib STATIC ${SOURCES})
