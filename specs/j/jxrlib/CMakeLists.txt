cmake_minimum_required(VERSION 3.5)
project(jxrlib C)
include(GNUInstallDirs)

set(JXRLIB_MAJOR 0)
set(JXRLIB_MINOR 0)

set(JXRLIB_LIB_VERSION ${JXRLIB_MAJOR}.${JXRLIB_MINOR}.0)
set(JXRLIB_SO_VERSION ${JXRLIB_MAJOR})

include(TestBigEndian)
test_big_endian(ISBIGENDIAN)
if(ISBIGENDIAN)
  set(DEF_ENDIAN -D_BIG__ENDIAN_)
endif()

add_definitions(-D__ANSI__ -DDISABLE_PERF_MEASUREMENT ${DEF_ENDIAN})

include_directories(
  common/include
  image/sys
  jxrgluelib
  jxrtestlib
)

# JXR Library
file(GLOB jpegxr_SRC image/sys/*.c image/decode/*.c image/encode/*.c)
file(GLOB jpegxr_HDR image/sys/*.h image/decode/*.h image/encode/*.h)

add_library(jpegxr ${jpegxr_SRC} ${jpegxr_HDR})
set_target_properties(jpegxr PROPERTIES VERSION ${JXRLIB_LIB_VERSION} SOVERSION ${JXRLIB_SO_VERSION})

install(TARGETS jpegxr
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# JXR-GLUE Library
file(GLOB jxrglue_SRC jxrgluelib/*.c jxrtestlib/*.c)
file(GLOB jxrglue_HDR jxrgluelib/*.h jxrtestlib/*.h)

add_library(jxrglue ${jxrglue_SRC} ${jxrglue_HDR})
set_target_properties(jxrglue PROPERTIES VERSION ${JXRLIB_LIB_VERSION} SOVERSION ${JXRLIB_SO_VERSION})
target_link_libraries(jxrglue jpegxr m)

install(TARGETS jxrglue
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

# JxrEncApp Executable
add_executable(JxrEncApp jxrencoderdecoder/JxrEncApp.c)
target_link_libraries(JxrEncApp jxrglue)
install(TARGETS JxrEncApp RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

# JxrDecApp Executable
add_executable(JxrDecApp jxrencoderdecoder/JxrDecApp.c)
target_link_libraries(JxrDecApp jxrglue)
install(TARGETS JxrDecApp RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})

# Headers
install(FILES jxrgluelib/JXRGlue.h jxrgluelib/JXRMeta.h jxrtestlib/JXRTest.h image/sys/windowsmediaphoto.h
  DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/jxrlib
)
install(DIRECTORY common/include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/jxrlib
  FILES_MATCHING PATTERN "*.h"
)
