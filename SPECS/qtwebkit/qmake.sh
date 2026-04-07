#!/bin/sh

qmake-qt4 \
  $@ \
  QMAKE_CFLAGS="${CFLAGS}" \
  QMAKE_CXXFLAGS="${CXXFLAGS}" \
  QMAKE_LFLAGS="${LDFLAGS}" \
