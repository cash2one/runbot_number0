# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/build

# Include any dependencies generated for this target.
include CMakeFiles/stereovision.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/stereovision.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/stereovision.dir/flags.make

CMakeFiles/stereovision.dir/src/stereovision.cpp.o: CMakeFiles/stereovision.dir/flags.make
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: ../src/stereovision.cpp
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: ../manifest.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/cpp_common/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/rostime/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/rosconsole/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/roscpp_traits/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/roscpp_serialization/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/genmsg/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/genpy/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/message_runtime/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/std_msgs/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/rosgraph_msgs/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/xmlrpcpp/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/roscpp/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/message_filters/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/console_bridge/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/class_loader/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/catkin/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/rospack/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/roslib/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/pluginlib/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/geometry_msgs/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/sensor_msgs/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/image_transport/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/opencv2/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/cv_bridge/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/camera_calibration_parsers/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/camera_info_manager/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/bond/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/smclib/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/bondcpp/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/share/nodelet/package.xml
CMakeFiles/stereovision.dir/src/stereovision.cpp.o: /opt/ros/groovy/stacks/camera_umd/uvc_camera/manifest.xml
	$(CMAKE_COMMAND) -E cmake_progress_report /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/build/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/stereovision.dir/src/stereovision.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -W -Wall -Wno-unused-parameter -fno-strict-aliasing -pthread -o CMakeFiles/stereovision.dir/src/stereovision.cpp.o -c /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/src/stereovision.cpp

CMakeFiles/stereovision.dir/src/stereovision.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/stereovision.dir/src/stereovision.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -W -Wall -Wno-unused-parameter -fno-strict-aliasing -pthread -E /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/src/stereovision.cpp > CMakeFiles/stereovision.dir/src/stereovision.cpp.i

CMakeFiles/stereovision.dir/src/stereovision.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/stereovision.dir/src/stereovision.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -W -Wall -Wno-unused-parameter -fno-strict-aliasing -pthread -S /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/src/stereovision.cpp -o CMakeFiles/stereovision.dir/src/stereovision.cpp.s

CMakeFiles/stereovision.dir/src/stereovision.cpp.o.requires:
.PHONY : CMakeFiles/stereovision.dir/src/stereovision.cpp.o.requires

CMakeFiles/stereovision.dir/src/stereovision.cpp.o.provides: CMakeFiles/stereovision.dir/src/stereovision.cpp.o.requires
	$(MAKE) -f CMakeFiles/stereovision.dir/build.make CMakeFiles/stereovision.dir/src/stereovision.cpp.o.provides.build
.PHONY : CMakeFiles/stereovision.dir/src/stereovision.cpp.o.provides

CMakeFiles/stereovision.dir/src/stereovision.cpp.o.provides.build: CMakeFiles/stereovision.dir/src/stereovision.cpp.o

# Object files for target stereovision
stereovision_OBJECTS = \
"CMakeFiles/stereovision.dir/src/stereovision.cpp.o"

# External object files for target stereovision
stereovision_EXTERNAL_OBJECTS =

../lib/libstereovision.so: CMakeFiles/stereovision.dir/src/stereovision.cpp.o
../lib/libstereovision.so: CMakeFiles/stereovision.dir/build.make
../lib/libstereovision.so: CMakeFiles/stereovision.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX shared library ../lib/libstereovision.so"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/stereovision.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/stereovision.dir/build: ../lib/libstereovision.so
.PHONY : CMakeFiles/stereovision.dir/build

CMakeFiles/stereovision.dir/requires: CMakeFiles/stereovision.dir/src/stereovision.cpp.o.requires
.PHONY : CMakeFiles/stereovision.dir/requires

CMakeFiles/stereovision.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/stereovision.dir/cmake_clean.cmake
.PHONY : CMakeFiles/stereovision.dir/clean

CMakeFiles/stereovision.dir/depend:
	cd /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/build /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/build /opt/ros/groovy/stacks/ros_workspace/src/OpenQbo/qbo_camera-master/build/CMakeFiles/stereovision.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/stereovision.dir/depend

