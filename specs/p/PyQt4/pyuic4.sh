#!/bin/sh
@PYTHON3@ -Ic "import PyQt4" &> /dev/null
if [ $? -eq 0 ]; then
  exec @PYTHON3@ -Im PyQt4.uic.pyuic ${1+"$@"}
else
  exec @PYTHON2@ -c "import sys; del sys.path[0]; import PyQt4.uic.pyuic; PyQt4.uic.pyuic.main()" ${1+"$@"}
fi
