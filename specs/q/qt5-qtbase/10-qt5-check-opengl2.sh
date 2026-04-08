#!/bin/bash

if [ -z "$QT_XCB_FORCE_SOFTWARE_OPENGL" ]; then

QT5_CHECK_OPENGL_VERSION=`LANG=C glxinfo 2> /dev/null | grep '^OpenGL version string: ' | head -n 1 | sed -e 's/^OpenGL version string: \([0-9]\).*$/\1/g'` ||:

if [ "$QT5_CHECK_OPENGL_VERSION" == "1" ]; then
  QT_XCB_FORCE_SOFTWARE_OPENGL=1
  export QT_XCB_FORCE_SOFTWARE_OPENGL
fi

unset QT5_CHECK_OPENGL_VERSION

fi
