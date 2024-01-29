#!/bin/sh

# An attempt at providing a qmake wrapper for projects that 
# lack native qmake support (ie, qmake is run by buildsystem
# instead of developer or fedora packager).

QMAKE="$(rpm --eval %{_qt_qmake})"
QMAKE_FLAGS="$(rpm --eval %{?_qt_qmake_flags})"

eval $QMAKE $QMAKE_FLAGS $@
