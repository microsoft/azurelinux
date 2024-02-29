#!/bin/bash

####   TESTING DISCLAIMER   ####
# This script follows the steps to run the tests for RabbitMQ v3.11.9 as of 2/22/23 on CBL-Mariner. As a result, this script can likely 
# be used as a baseline to execute the test for future releases/upgrades to verify the package integrity. That said, some things may need
# to be updated in order to make the tests succeed such as updating the links for erlang, elixir, bazel, and/or mandoc in order to have
# some or all tests succeed.
#
# Additionally, there are 3 tests that remain as failutres due to some additional dependencies on large packages 'aws' and 'dotnet', or in
# one case, an excluded command from openldap 'slapd' (see //SPECS/openldap/openldap.spec for details). With the other 506 test suites 
# passing, I decided to leave these as is since they also don't impact the running of the entire test suite.
#
# The 3 expected failures are the following:
# //deps/rabbitmq_peer_discovery_aws:integration_SUITE
# //deps/rabbitmq_auth_backend_ldap:system_SUITE
# //deps/rabbitmq_ampq1_0:system_SUITE - shard 1 of 2 specifically
#
# RabbitMQ depends on bazel 'latest'. As of 2/22/23, the latest bazel version is '6.0.0'.
#
# Some tests also rely on the 'mandoc' package. As of 2/22/23, this package was not available in Mariner. As a result, the package is
# pulled from source and installed. These test break the entire run, so this dependency must be pulled in for the entire suite to succeed.
#
# The elixir package relies on having the UTF-8 character encoding set in your locale in order to function properly. Because of this, you 
# set bazel to use the UTF-8 locale that you'd like with the --test-env flag at runtime, unless UTF-8 is the true system default (in this case
# no additional flags are needed at runtime for elixir).
#
# Be sure to check the rabbitmq official repository for any testing updates before executing this script in case the process has changed in
# any capacity or become more well documentated:
#   README.md: https://github.com/rabbitmq/rabbitmq-server/blob/main/README.md
#   BAZEL.md:  https://github.com/rabbitmq/rabbitmq-server/blob/main/BAZEL.md
#
#### END TESTING DISCLAIMER ####

####   SCRIPT ASSUMPTIONS   ####
# The following line has been added to `$RABBIT_MQ_DIR/.bazelrc`:
#   build --cache_test_results=no
#
# `$RABBIT_MQ_DIR/user.bazelrc` has been created and updated from the `user-template.bazelrc` in the rabbitmq repo.
# 
# This script should be run with `sudo` or with similar root access to directories like /usr/local/bin and /usr/local/sbin
#
# The PARENT_DIR variable must be set to the parent directory of your rabbitmq directory.
#### END SCRIPT ASSUMPTIONS ####

# Setup Path Variables
PARENT_DIR="/path/to/rabbitmq/parent/directory" # <------ SET ME!!!!!
RABBIT_MQ_DIR="$PARENT_DIR/rabbitmq"
BAZEL_DIR="$PARENT_DIR/bazel-src"
MANDOC_DIR="$PARENT_DIR/mandoc"
DAEMONIZE_DIR="$PARENT_DIR/daemonize"

BAZEL_INSTALL_DIR="/usr/local/bin"

# Store old PATH to restore later
EXISTING_USER_PATH="$PATH"

# Print out config variables
echo "#### CONFIG DIRECTORY VARS ####"
echo "PARENT_DIR:           $PARENT_DIR"
echo "RABBIT_MQ_DIR:        $RABBIT_MQ_DIR"
echo "BAZEL_DIR:            $BAZEL_DIR"
echo "MANDOC_DIR            $MANDOC_DIR"
echo "DAEMONIZE_DIR         $DAEMONIZE_DIR"
echo "EXISTING_USER_PATH:   $EXISTING_USER_PATH"
echo ""
echo ""


# Remove existing/old test directories
rm -rf $BAZEL_DIR $MANDOC_DIR $DAEMONIZE_DIR

# Required dependencies are installed
dnf install msopenjdk-11 wget git build-essential python3 zip unzip

# Get Dependency sources
wget https://github.com/bazelbuild/bazel/releases/download/6.0.0/bazel-6.0.0-dist.zip
wget https://mandoc.bsd.lv/snapshots/mandoc-1.14.6.tar.gz
git clone http://github.com/bmc/daemonize.git

# Install bazel 6.0.0
mkdir $BAZEL_DIR
mv bazel-6.0.0-dist.zip $BAZEL_DIR/bazel-6.0.0-dist.zip
pushd $BAZEL_DIR
unzip bazel-6.0.0-dist.zip
env EXTRA_BAZEL_ARGS="--tool_java_runtime_version=local_jdk" bash ./compile.sh
cp output/bazel $BAZEL_INSTALL_DIR/bazel
popd

# Install mandoc 1.14.6
mkdir $MANDOC_DIR
mv mandoc-1.14.6.tar.gz $MANDOC_DIR/mandoc-1.14.6.tar.gz
pushd $MANDOC_DIR
tar -zxvf mandoc-1.14.6.tar.gz
cd mandoc-1.14.6
make
make install
popd

# Install daemonize 1.7.8
pushd $DAEMONIZE_DIR
sh configure
make
make install
export PATH="$PATH:/usr/local/sbin"
popd

# Make and install rabbitmq
pushd $RABBIT_MQ_DIR
make distclean
make
make install
popd

# Run tests using bazel
pushd $RABBIT_MQ_DIR
bazel clean
bazel test //... --test_env="LC_ALL=en_US.UTF-8"
popd

# Restore PATH to original state
export PATH="$EXISTING_USER_PATH"
rm $BAZEL_INSTALL_DIR/bazel
