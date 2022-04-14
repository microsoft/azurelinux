#!/bin/sh
# 
# Xerces-J2 version script
# JPackage Project (http://www.jpackage.org/)
# $Id$

# Source functions library
. /usr/share/java-utils/java-functions

# Configuration
MAIN_CLASS=org.apache.xerces.impl.Version

# Set parameters
set_jvm
export CLASSPATH=$(build-classpath xerces-j2)
set_flags $BASE_FLAGS
set_options $BASE_OPTIONS

# Let's start
run "$@"
