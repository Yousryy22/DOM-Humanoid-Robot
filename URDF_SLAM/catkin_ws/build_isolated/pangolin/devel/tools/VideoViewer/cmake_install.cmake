# Install script for directory: /home/user/catkin_ws/src/Pangolin/tools/VideoViewer

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/user/catkin_ws/devel_isolated/pangolin")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer"
         RPATH "")
  endif()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
file(INSTALL DESTINATION "/home/user/catkin_ws/devel_isolated/pangolin/bin" TYPE EXECUTABLE FILES "/home/user/catkin_ws/build_isolated/pangolin/devel/tools/VideoViewer/VideoViewer")
  if(EXISTS "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer"
         OLD_RPATH "/home/user/catkin_ws/build_isolated/pangolin/devel:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/user/catkin_ws/devel_isolated/pangolin/bin/VideoViewer")
    endif()
  endif()
endif()

