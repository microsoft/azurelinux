cmake_minimum_required(VERSION 3.5)

project(giflib C)
include(GNUInstallDirs)

SET(BUILD_STATIC_LIBS OFF CACHE BOOL "Whether to also build static libs")

execute_process(COMMAND ./getversion
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    OUTPUT_VARIABLE VERSION
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

set(LIBMAJOR 7)
set(LIBMINOR 1)
set(LIBPOINT 0)
set(LIBVER "${LIBMAJOR}.${LIBMINOR}.${LIBPOINT}")

set(giflib_SRC
    dgif_lib.c
    egif_lib.c
    getarg.c
    gifalloc.c
    gif_err.c
    gif_font.c
    gif_hash.c
    openbsd-reallocarray.c
    qprintf.c
    quantize.c
)

# Some utilities are installed
set(giflib_INSTALLABLE
    gif2rgb
    gifbuild
    giffix
    giftext
    giftool
    gifclrmp
)

# Some utilities are only used internally for testing.
# There is a parallel list in doc/Makefile.
# These are all candidates for removal in future releases.
set(giflib_UTILS
    ${giflib_INSTALLABLE}
    gifbg
    gifcolor
    gifecho
    giffilter
    gifhisto
    gifinto
    gifwedge
)

file(GLOB giflib_MAN doc/*.1)

### Build library / tools

add_library(gif SHARED ${giflib_SRC})
target_link_libraries(gif m)
set_target_properties(gif PROPERTIES VERSION ${LIBVER} SOVERSION ${LIBMAJOR})
if(WIN32)
    set_target_properties(gif PROPERTIES SUFFIX "-${LIBMAJOR}${CMAKE_SHARED_LIBRARY_SUFFIX}")
endif(WIN32)

if(${BUILD_STATIC_LIBS})
    add_library(gif_static STATIC ${giflib_SRC})
    set_target_properties(gif_static PROPERTIES OUTPUT_NAME gif)
endif(${BUILD_STATIC_LIBS})


foreach(UTILITY ${giflib_UTILS})
    add_executable(${UTILITY} ${UTILITY}.c)
    target_link_libraries(${UTILITY} gif)
endforeach()

### Installation

install(TARGETS gif
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

if(${BUILD_STATIC_LIBS})
    install(TARGETS gif_static ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR})
endif(${BUILD_STATIC_LIBS})

foreach(UTILITY ${giflib_UTILS})
    install(TARGETS ${UTILITY} DESTINATION ${CMAKE_INSTALL_BINDIR})
endforeach()

install(FILES gif_lib.h gif_getarg.h DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})
install(FILES ${giflib_MAN} DESTINATION ${CMAKE_INSTALL_MANDIR}/man1)


### Distribution tarball
set(giflib_DIST
    *.c
    *.h
    README
    NEWS
    TODO
    COPYING
    getversion
    ChangeLog
    CMakeLists.txt
    build.adoc
    history.adoc
    control
    doc/whatsinagif
    doc/*.1
    doc/*.xml
    doc/*.txt
    doc/index.html.in
    doc/00README
    doc/Makefile
    tests
    pic
)
# We include all of the XML, and also generated manual pages
# so people working from the distribution tarball won't need xmlto.
add_custom_target(dist-gz
    COMMAND tar --transform='s:^:giflib-${VERSION}/:' -czf giflib-${VERSION}.tar.gz ${giflib_DIST}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

add_custom_target(dist-bz2
    COMMAND tar --transform='s:^:giflib-${VERSION}/:' -cjf giflib-${VERSION}.tar.bz2 ${giflib_DIST}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

add_custom_target(dist DEPENDS dist-gz DEPENDS dist-bz2)


### Auditing tools

# cppcheck should run clean
add_custom_target(cppcheck
    COMMAND cppcheck --inline-suppr --template gcc --enable=all --suppress=unusedFunction --force *.[ch]
)
