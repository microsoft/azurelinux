cmake_minimum_required(VERSION 3.5)
project(qcustomplot)
include(GNUInstallDirs)

set(LIB_VER "" CACHE STRING "Library version")
set(QT_VER "6" CACHE STRING "Target Qt version")

set(QCUSTOMPLOT_LIB_VERSION ${LIB_VER})
string(REPLACE "." ";" VERSION_LIST ${LIB_VER})
list(GET VERSION_LIST 0 QCUSTOMPLOT_SO_VERSION)

FIND_PACKAGE(Qt${QT_VER}Core REQUIRED)
FIND_PACKAGE(Qt${QT_VER}Gui REQUIRED)
FIND_PACKAGE(Qt${QT_VER}Widgets REQUIRED)
FIND_PACKAGE(Qt${QT_VER}PrintSupport REQUIRED)
SET(CMAKE_AUTOMOC ON)

# Library
add_library(qcustomplot SHARED qcustomplot.cpp qcustomplot.h)
set_target_properties(qcustomplot PROPERTIES VERSION ${QCUSTOMPLOT_LIB_VERSION} SOVERSION ${QCUSTOMPLOT_SO_VERSION})
if (${QT_VER} GREATER "4")
set_target_properties(qcustomplot PROPERTIES OUTPUT_NAME qcustomplot-qt${QT_VER})
endif()
target_link_libraries(qcustomplot Qt${QT_VER}::Core Qt${QT_VER}::Gui Qt${QT_VER}::Widgets Qt${QT_VER}::PrintSupport)

install(TARGETS qcustomplot
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# Headers
install(FILES qcustomplot.h
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)
