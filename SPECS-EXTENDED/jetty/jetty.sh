#!/usr/bin/env bash
# Configuration files
#
# /etc/default/jetty
#   If it exists, this is read at the start of script. It may perform any
#   sequence of shell commands, like setting relevant environment variables.
#
# /etc/jetty.conf
#   If found, and no configurations were given on the command line,
#   the file will be used as this script's configuration.
#   Each line in the file may contain:
#     - A comment denoted by the pound (#) sign as first non-blank character.
#     - The path to a regular file, which will be passed to jetty as a
#       config.xml file.
#     - The path to a directory. Each *.xml file in the directory will be
#       passed to jetty as a config.xml file.
#     - All other lines will be passed, as-is to the start.jar
#
#   The files will be checked for existence before being passed to jetty.
#
# Configuration variables
#
# JAVA
#   Command to invoke Java. If not set, java (from the PATH) will be used.
#
# JAVA_OPTIONS
#   Extra options to pass to the JVM
#
# JETTY_HOME
#   Where Jetty is installed. If not set, the script will try go
#   guess it by first looking at the invocation path for the script,
#   and then by looking in standard locations as $HOME/opt/jetty
#   and /opt/jetty. The java system property "jetty.home" will be
#   set to this value for use by configure.xml files, f.e.:
#
#    <Arg><Property name="jetty.home" default="."/>/webapps/jetty.war</Arg>
#
# JETTY_BASE
#   Where your Jetty base directory is.  If not set, the value from
#   $JETTY_HOME will be used.
#
# JETTY_ARGS
#   The default arguments to pass to jetty.
#   For example
#      JETTY_ARGS=jetty.port=8080 jetty.spdy.port=8443 jetty.secure.port=443
#

set -e -C

readConfig()
{
  echo "Reading $1.."
  source "$1"
}

CONFIGS=()

if [ -f /etc/default/jetty ]; then
  readConfig /etc/default/jetty
fi

if [ -z "$JETTY_HOME" ]; then
    JETTY_HOME=/usr/share/jetty
fi

if [ -z "$JETTY_BASE" ]; then
  JETTY_BASE="$JETTY_HOME"
fi

cd "$JETTY_BASE"
JETTY_BASE="$PWD"

if [ -z "$JETTY_CONF" ]
then
  JETTY_CONF=/etc/jetty.conf
fi

if [ -f "$JETTY_CONF" ] && [ -r "$JETTY_CONF" ]
then
  while read -r CONF
  do
    if expr "$CONF" : '#' >/dev/null ; then
      continue
    fi

    if [ -d "$CONF" ]
    then
      # assume it's a directory with configure.xml files
      # for example: /etc/jetty.d/
      # sort the files before adding them to the list of JETTY_ARGS
      for XMLFILE in "$CONF/"*.xml
      do
        if [ -r "$XMLFILE" ] && [ -f "$XMLFILE" ]
        then
          JETTY_ARGS+=("$XMLFILE")
        else
          echo "** WARNING: Cannot read '$XMLFILE' specified in '$JETTY_CONF'"
        fi
      done
    else
      # assume it's a command line parameter (let start.jar deal with its validity)
      JETTY_ARGS+=("$CONF")
    fi
  done < "$JETTY_CONF"
fi

if [ -z "$JAVA" ]
then
    . /usr/share/java-utils/java-functions
    set_jvm
    set_javacmd
    JAVA="$JAVACMD"
fi

if [ -z "$JETTY_LOGS" ] && [ -d $JETTY_BASE/logs ]
then
  JETTY_LOGS=/var/log/jetty/logs
fi
JAVA_OPTIONS+=("-Djetty.logs=$JETTY_LOGS")

JAVA_OPTIONS+=("-Djetty.home=$JETTY_HOME" "-Djetty.base=$JETTY_BASE")

JETTY_START="$JETTY_HOME/start.jar"
START_INI="$JETTY_BASE/start.ini"
if [ ! -f "$START_INI" ]
then
  echo "Cannot find a start.ini in your JETTY_BASE directory: $JETTY_BASE" 2>&2
  exit 1
fi

RUN_ARGS=(${JAVA_OPTIONS[@]} -jar "$JETTY_START" ${JETTY_ARGS[*]})
RUN_CMD=("$JAVA" ${RUN_ARGS[@]})

echo -n "Starting Jetty: "
${RUN_CMD[*]}
