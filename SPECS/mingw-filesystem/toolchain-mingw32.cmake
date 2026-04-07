SET(CMAKE_SYSTEM_NAME Windows)
SET(CMAKE_SYSTEM_PROCESSOR x86)

# specify the cross compiler
IF(NOT DEFINED ENV{CC})
    SET(CMAKE_C_COMPILER i686-w64-mingw32-gcc)
ENDIF()
IF(NOT DEFINED ENV{CXX})
    SET(CMAKE_CXX_COMPILER i686-w64-mingw32-g++)
ENDIF()
IF(NOT DEFINED ENV{FC})
    SET(CMAKE_Fortran_COMPILER i686-w64-mingw32-gfortran)
ENDIF()

# where is the target environment
SET(CMAKE_FIND_ROOT_PATH /usr/i686-w64-mingw32/sys-root/mingw)

# search for programs in the build host directories
SET(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
# for libraries, headers and packages in the target directories
SET(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
SET(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)

# Make sure Qt can be detected by CMake
SET(QT_BINARY_DIR /usr/i686-w64-mingw32/bin /usr/bin)

# set the resource compiler (RHBZ #652435)
IF(NOT $ENV{RC})
    SET(CMAKE_RC_COMPILER /usr/bin/i686-w64-mingw32-windres)
ENDIF()

# These are needed for compiling lapack (RHBZ #753906)
SET(CMAKE_AR:FILEPATH /usr/bin/i686-w64-mingw32-ar)
SET(CMAKE_RANLIB:FILEPATH /usr/bin/i686-w64-mingw32-ranlib)

# Workaround failure to detect boost (see #2037724)
SET(Boost_ARCHITECTURE "-x32")
