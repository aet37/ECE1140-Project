cmake_minimum_required(VERSION 3.10)

### Require out-of-source builds
file(TO_CMAKE_PATH "${PROJECT_BINARY_DIR}/CMakeLists.txt" LOC_PATH)
if(EXISTS "${LOC_PATH}")
    message(FATAL_ERROR "You cannot build in a source directory (or any directory with a CMakeLists.txt file). Please make a build subdirectory. Feel free to remove CMakeCache.txt and CMakeFiles.")
endif()

# Set the project name
project(ECE1140_Project)

# Enable testing
enable_testing()

# Add source subdirectory
add_subdirectory(src)
add_subdirectory(tests/UnitTests)