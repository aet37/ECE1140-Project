# Find boost
find_package(Boost 1.53.0 COMPONENTS system)

# Set include directory
include_directories("${PROJECT_SOURCE_DIR}/include/Server")
include_directories("${PROJECT_SOURCE_DIR}/include/HWTrackController")
include_directories("${Boost_INCLUDE_DIRS}")

# Add subdirectories
add_subdirectory(HWTrackController)

# Set source files
set(SOURCES
    Server/ConnectionHandler.cpp
    Server/Server.cpp
    Main.cpp
)

add_executable(main ${SOURCES})

target_link_libraries(main ${Boost_LIBRARIES} HWTrackController)
