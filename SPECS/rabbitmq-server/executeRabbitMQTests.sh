#!/bin/bash

####   TESTING DISCLAIMER   ####
# This script follows the steps to run the tests for RabbitMQ v3.13.0 as of 4/1/24 on Azure Linux. As a result, this script can likely 
# be used as a baseline to execute the test for future releases/upgrades to verify the package integrity. That said, some things may need
# to be updated in order to make the tests succeed such as updating the links for erlang, elixir, bazel, and/or mandoc in order to have
# some or all tests succeed.
#
# Additionally, there are 3 tests that remain as failutres due to some additional dependencies on large packages 'aws' and 'dotnet', or in
# one case, an excluded command from openldap 'slapd' (see //SPECS/openldap/openldap.spec for details). With the other test suites 
# passing, I decided to leave these as is since they also don't impact the running of the entire test suite.
#
# The 3 expected failures are the following:
# //deps/rabbitmq_peer_discovery_aws:integration_SUITE
# //deps/rabbitmq_auth_backend_ldap:system_SUITE
# //deps/rabbitmq_ampq1_0:system_SUITE - shard 1 of 2 specifically
#
# Additional failures in v3.13.0: 
# //deps/rabbit:feature_flags_with_unprivileged_user_SUITE-mixed - both shards fail for Assertion error
# //deps/rabbit:feature_flags_with_unprivileged_user_SUITE - both shards fail for Assertion error
# //deps/rabbit:feature_flag_v2_SUITE - rpc_calls Assertion error
# //deps/rabbit:per_vhost_msg_store_SUITE - badmatch(?)
# //deps/rabbit:per_vhost_msg_store_SUITE-mixed - badmatch(?)
# //deps/rabbitmq_federation:federation_status_command_SUITE - Condition did not materialize in the expected period of time (aka timeout)
# //deps/rabbitmq_federation:federation_status_command_SUITE-mixed - Condition did not materialize in the expected period of time (aka timeout)

# Skipped tests:
# //deps/rabbitmq_cli:check_formatted
# //deps/rabbitmq_cli:compile_warnings_as_errors
#
# RabbitMQ depends on bazel 'latest'. This can be updated as needed using the "BAZEL_DEP_VERSION" variable for the purposes of this script
#
# Some tests also rely on the 'mandoc' package. As of 4/1/24, this package was not available in Azure Linux. As a result, the package is
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
# This test generates A LOT of files, you will need 2.6M+ inodes to run the full SUITE. (aka about 50GB free in ext4 filesystem)
#
# You have pulled the rabbitmq source from github as it contains additional bazel build files which our normal source does not
# (And checked out the appropriate tag + applied any local patches from Azure Linux)
#
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

BAZEL_DEP_VERSION="7.1.1"
MANDOC_DEP_VERSION="1.14.6"

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

# Ensure rabbitmq deps are installed
tdnf install -y erlang elixir libxslt xmlto python python3-simplejson zip unzip rsync glibc-lang

# Required dependencies are installed
tdnf install -y msopenjdk-17 wget git build-essential python python-pip zip unzip kernel-headers binutils zlib-devel

# Get Dependency sources
wget https://github.com/bazelbuild/bazel/releases/download/$BAZEL_DEP_VERSION/bazel-$BAZEL_DEP_VERSION-dist.zip
wget https://mandoc.bsd.lv/snapshots/mandoc-$MANDOC_DEP_VERSION.tar.gz
git clone http://github.com/bmc/daemonize.git

# Install bazel
mkdir $BAZEL_DIR
mv bazel-$BAZEL_DEP_VERSION-dist.zip $BAZEL_DIR/bazel-$BAZEL_DEP_VERSION-dist.zip
pushd $BAZEL_DIR
unzip bazel-$BAZEL_DEP_VERSION-dist.zip
env EXTRA_BAZEL_ARGS="--tool_java_runtime_version=local_jdk" bash ./compile.sh
cp output/bazel $BAZEL_INSTALL_DIR/bazel
popd

# Install mandoc
mkdir $MANDOC_DIR
mv mandoc-$MANDOC_DEP_VERSION.tar.gz $MANDOC_DIR/mandoc-$MANDOC_DEP_VERSION.tar.gz
pushd $MANDOC_DIR
tar -zxvf mandoc-$MANDOC_DEP_VERSION.tar.gz
cd mandoc-$MANDOC_DEP_VERSION
sh configure
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
# --noincompatible_sandbox_hermetic_tmp is required for runs due to flakey(?) failures noticed during
# runs of this script for when using bazel-7.1.1. These failures had 'ebin' notied as a "dangling
# symbolic link" causing most tests to not even start without the added flag. Azure Linux does not have 
# support for older jdk versions nor older bazel versions as a result so we cannot roll back to 6.4.0 
# before the issue was present upstream.
# See the below issues for details:
#   Actual Error: https://github.com/bazelbuild/bazel/issues/20886
#   Workaround: https://github.com/bazelbuild/bazel/issues/21215
bazel test //... --test_env="LC_ALL=en_US.UTF-8" --noincompatible_sandbox_hermetic_tmp
popd

# Restore PATH to original state
export PATH="$EXISTING_USER_PATH"
rm $BAZEL_INSTALL_DIR/bazel
