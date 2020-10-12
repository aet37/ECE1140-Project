# Find catch2
find_package(Catch2 REQUIRED)
find_package(Threads REQUIRED)

# Add subdirectories
add_subdirectory(Common)
add_subdirectory(HWTrackController)
add_subdirectory(CTC)
add_subdirectory(SWTrackController)