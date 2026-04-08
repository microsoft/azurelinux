## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 55;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# We need to use C++17 to link against the system abseil-cpp, since it was
# compiled with C++17 (an intentional abseil-cpp design decision).
%global cpp_std 17

# However, we also get linker errors building the tests if we link against the
# copy of gtest in Fedora (compiled with C++11). The exact root cause is not
# quite clear. We must therefore bundle a copy of gtest in the source RPM
# rather than using the system copy. This is to be discouraged, but there is no
# alternative in this case. It is not treated as a bundled library because it
# is used only at build time, and contributes nothing to the installed files.
# We take measures to verify this in %%check. As long as we are using our own
# copy, we use the exact same version as upstream.
%global gtest_url https://github.com/google/googletest
%global gtest_dir googletest-%{gtest_commit}
%global gtest_commit 0e402173c97aea7a00749e825b194bfede4f2e45
#global gtest_version 1.11.0
#global gtest_dir googletest-release-#{gtest_version}
%bcond system_gtest        0

# =====

# Parameters for third-party sources needed for their .proto files, which
# upstream expects to download at build time.
#
# See https://github.com/grpc/grpc/pull/29254 “[xDS Proto] Enhence gRPC
# buildgen for 3rd party proto compilation” and
# https://github.com/grpc/grpc/commit/99752b173cfa2fba81dedb482ee4fd74b2a46bb0,
# in which the download mechanism was added.
#
# Check CMakeLists.txt (search for “download_archive”) for a list of these
# third-party sources and the commit hashes used in the grpc release.
#
# Note that we do not treat these additional sources as bundled dependencies,
# since (provably) only the .proto files are used.
#
# In practice, it seems the generated binding code for these protos is not
# re-generated when building this package, so we could get by with creating the
# appropriate directories and touching an empty file within each. We include
# these archives in the source RPM anyway, since they are in some sense part of
# the original sources for the generated proto code.

# This will probably never be separately packaged in Fedora, since upstream can
# only build with Bazel (and Bazel is such a mess of bundled dependencies that
# it is unlikely to every be successfully packaged under the Fedora packaging
# guidelines. Note that the URL is a read-only mirror based on
# https://github.com/envoyproxy/envoy, with different commit hashes.
%global envoy_api_commit 9c42588c956220b48eb3099d186487c2f04d32ec
%global envoy_api_url https://github.com/envoyproxy/data-plane-api
%global envoy_api_dir data-plane-api-%{envoy_api_commit}

%global googleapis_commit 2f9af297c84c55c8b871ba4495e01ade42476c92
%global googleapis_url https://github.com/googleapis/googleapis
%global googleapis_dir googleapis-%{googleapis_commit}

%global opencensus_proto_version 0.3.0
%global opencensus_proto_url https://github.com/census-instrumentation/opencensus-proto
%global opencensus_proto_dir opencensus-proto-%{opencensus_proto_version}

%global xds_commit cb28da3451f158a947dfc45090fe92b07b243bc1
%global xds_url https://github.com/cncf/xds
%global xds_dir xds-%{xds_commit}

# =====

# This must be enabled to get grpc_cli, which is apparently considered part of
# the tests by upstream. This is mentioned in
# https://github.com/grpc/grpc/issues/23432.
%bcond core_tests          1

# A great many of these tests (over 20%) fail. Any help in understanding these
# well enough to fix them or report them upstream is welcome.
%bcond python_aio_tests    0

%ifnarch s390x
# There are currently a significant number of failures like:
#
#   Exception serializing message!
#   Traceback (most recent call last):
#     File "/builddir/build/BUILDROOT/grpc-1.48.0-2.fc38~bootstrap.x86_64/usr/lib64/python3.11/site-packages/grpc/_common.py", line 86, in _transform
#       return transformer(message)
#              ^^^^^^^^^^^^^^^^^^^^
#     File "/usr/lib/python3.11/site-packages/google/protobuf/internal/python_message.py", line 1082, in SerializeToString
#       if not self.IsInitialized():
#              ^^^^^^^^^^^^^^^^^^
#   AttributeError: 'NoneType' object has no attribute 'IsInitialized'
%bcond python_gevent_tests 0
%else
# A significant number of Python tests pass in test_lite but fail in
# test_gevent, mostly by dumping core without a traceback.  Since it is tedious
# to enumerate these (and it is difficult to implement “suite-specific” skips
# for shared tests, so the tests would have to be skipped in all suites), we
# just skip the gevent suite entirely on this architecture.
%bcond python_gevent_tests 0
%endif

# Running core tests under valgrind may help debug crashes. This is mostly
# ignored if the gdb build conditional is also set.
%bcond valgrind            0
# Running core tests under gdb may help debug crashes.
%bcond gdb                 0

# HTML documentation generated with Doxygen and/or Sphinx is not suitable for
# packaging due to a minified JavaScript bundle inserted by
# Doxygen/Sphinx/Sphinx themes itself. See discussion at
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555.
#
# Normally we could consider enabling the Doxygen PDF documentation as a lesser
# substitute, but (after enabling it and working around some Unicode characters
# in the Markdown input) we get:
#
#   ! TeX capacity exceeded, sorry [main memory size=6000000].
#
# A similar situation applies to the Sphinx-generated HTML documentation for
# Python, except that we have not even tried to render it as a PDF because it
# is too unpleasant to try if we already cannot package the Doxygen-generated
# documentation. Instead, we have just dropped all documentation.

Name:           grpc
Version:        1.48.4
Release:        %autorelease
Summary:        RPC library and framework

%global srcversion %(echo '%{version}' | sed -r 's/~rc/-pre/')
%global pyversion %(echo '%{version}' | tr -d '~')

# CMakeLists.txt: gRPC_CORE_SOVERSION
%global c_so_version 26
# CMakeLists.txt: gRPC_CPP_SOVERSION
# See https://github.com/abseil/abseil-cpp/issues/950#issuecomment-843169602
# regarding unusual C++ SOVERSION style (not a single number).
%global cpp_so_version 1.48

# The entire source is Apache-2.0 except the following:
#
# BSD-2-Clause:
#   - third_party/xxhash is BSD-2-Clause, at least the relevant parts (not the
#     command-line tool); it is unbundled, but then it is used as a header-only
#     library due to XXH_INCLUDE_ALL, so we must treat it as a static library
#     and include its license in that of the binary RPMs
#     * Potentially linked into any compiled subpackage (but not pure-Python
#       subpackages, etc.)
# BSD-3-Clause:
#   - third_party/upb/, except third_party/upb/third_party/lunit/ and
#     third_party/upb/third_party/utf8_range/
#     * Potentially linked into any compiled subpackage (but not pure-Python
#       subpackages, etc.)
#   - third_party/address_sorting/
#     * Potentially linked into any compiled subpackage (but not pure-Python
#       subpackages, etc.)
# MIT:
#   - third_party/upb/third_party/utf8_range
#     * Potentially linked into any compiled subpackage (but not pure-Python
#       subpackages, etc.)
#
# as well as the following which do not contribute to the base License field or
# any subpackage License field for the reasons noted:
#
# MPL-2.0:
#   - etc/roots.pem
#     * Truncated to an empty file in prep; a symlink to the shared system
#       certificates is used instead
#   - src/android/test/interop/app/src/main/assets/roots.pem
#     * Truncated to an empty file in prep
# ISC:
#   - src/boringssl/boringssl_prefix_symbols.h
#     * Removed in prep; not used when building with system OpenSSL
# BSD-3-Clause:
#   - src/objective-c/*.podspec and
#     templates/src/objective-c/*.podspec.template
#     * Unused since the Objective-C bindings are not currently built;
#       furthermore, these seem to be build-system files that would not
#       contribute their licenses to the binary RPM contents anyway
# NTP:
#   - third_party/cares/ares_build.h
#     * Removed in prep; header from system C-Ares used instead
# MIT:
#   - third_party/upb/third_party/lunit/
#     * Removed in prep, since there is no obvious way to run the upb tests
License:        Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND MIT
URL:            https://www.grpc.io
%global forgeurl https://github.com/grpc/grpc/
Source0:        %{forgeurl}/archive/v%{srcversion}/grpc-%{srcversion}.tar.gz
Source1:        %{gtest_url}/archive/%{gtest_commit}/%{gtest_dir}.tar.gz
#Source1:        #{gtest_url}/archive/release-#{gtest_version}/#{gtest_dir}.tar.gz
Source2:        %{envoy_api_url}/archive/%{envoy_api_commit}/%{envoy_api_dir}.tar.gz
Source3:        %{googleapis_url}/archive/%{googleapis_commit}/%{googleapis_dir}.tar.gz
Source4:        %{opencensus_proto_url}/archive/v%{opencensus_proto_version}/%{opencensus_proto_dir}.tar.gz
Source5:        %{xds_url}/archive/%{xds_commit}/%{xds_dir}.tar.gz

# Downstream grpc_cli man pages; hand-written based on “grpc_cli help” output.
Source100:      grpc_cli.1
Source101:      grpc_cli-ls.1
Source102:      grpc_cli-call.1
Source103:      grpc_cli-type.1
Source104:      grpc_cli-parse.1
Source105:      grpc_cli-totext.1
Source106:      grpc_cli-tojson.1
Source107:      grpc_cli-tobinary.1
Source108:      grpc_cli-help.1

# ~~~~ C (core) and C++ (cpp) ~~~~

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
%if %{with core_tests}
# Used on grpc_cli:
BuildRequires:  chrpath
%endif

BuildRequires:  pkgconfig(zlib)
BuildRequires:  cmake(gflags)
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  protobuf-compiler
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(openssl)
%if ! (0%{?rhel} >= 10)
# https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
BuildRequires:  openssl-devel-engine
%endif
BuildRequires:  cmake(c-ares)
BuildRequires:  abseil-cpp-devel
# Sets XXH_INCLUDE_ALL, which means xxhash is used as a header-only library
BuildRequires:  pkgconfig(libxxhash)
BuildRequires:  xxhash-static

%if %{with core_tests}
BuildRequires:  cmake(benchmark)
%if %{with system_gtest}
BuildRequires:  cmake(gtest)
BuildRequires:  pkgconfig(gmock)
%endif
%if %{with valgrind}
BuildRequires:  valgrind
%endif
%if %{with gdb}
BuildRequires:  gdb
%endif
%endif

# ~~~~ Python ~~~~

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

# grpcio (setup.py) setup_requires (with
#     GRPC_PYTHON_ENABLE_DOCUMENTATION_BUILD, which is NOT enabled):
# BuildRequires:  python3dist(sphinx)

# grpcio (setup.py) setup_requires (with
#     GRPC_PYTHON_ENABLE_DOCUMENTATION_BUILD, which is NOT enabled):
# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
BuildRequires:  python3dist(six) >= 1.10
# grpcio (setup.py) install_requires also has:
#   six>=1.5.2

# grpcio (setup.py) setup_requires (with GRPC_PYTHON_BUILD_WITH_CYTHON, or
# absent generated sources); also needed for grpcio_tools
# (tools/distrib/python/grpcio_tools/setup.py)
BuildRequires: python3dist(cython) > 0.23

# grpcio (setup.py) install_requires:
# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
#   futures>=2.2.0; python_version<'3.2'

# grpcio (setup.py) install_requires:
# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
#   enum34>=1.0.4; python_version<'3.4'

# grpcio_csds (src/python/grpcio_csds/setup.py) install_requires:
# grpcio_channelz (src/python/grpcio_channelz/setup.py) install_requires:
# grpcio_health_checking (src/python/grpcio_health_checking/setup.py)
#     install_requires:
# grpcio_reflection (src/python/grpcio_reflection/setup.py) install_requires:
# grpcio_status (src/python/grpcio_status/setup.py) install_requires:
# grpcio_testing (src/python/grpcio_testing/setup.py) install_requires:
# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
# grpcio_tools (tools/distrib/python/grpcio_tools/setup.py) install_requires:
BuildRequires:  python3dist(protobuf) >= 3.12.0

# grpcio_status (src/python/grpcio_status/setup.py) install_requires:
BuildRequires:  python3dist(googleapis-common-protos) >= 1.5.5

# Several packages have dependencies on grpcio or grpcio_tools—and grpcio-tests
# depends on all of the other Python packages—which are satisfied within this
# package.
#
# Similarly, grpcio_admin depends on grpcio_channelz and grpcio_csds.

# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
BuildRequires:  python3dist(oauth2client) >= 1.4.7

# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
BuildRequires:  python3dist(google-auth) >= 1.17.2

# grpcio_tests (src/python/grpcio_tests/setup.py) install_requires:
BuildRequires:  python3dist(requests) >= 2.14.2

%if %{with python_gevent_tests}
# Required for “test_gevent” tests:
BuildRequires:  python3dist(gevent)
%endif

# For stopping the port server
BuildRequires:  curl

# ~~~~ Miscellaneous ~~~~

# https://bugzilla.redhat.com/show_bug.cgi?id=1893533
%global _lto_cflags %{nil}

# Reference documentation, which is *not* enabled
# BuildRequires:  doxygen

BuildRequires:  ca-certificates
# For converting absolute symlinks in the buildroot to relative ones
BuildRequires:  symlinks
# For hardlinking duplicate files in the examples
BuildRequires:  hardlink

# Apply Fedora system crypto policies. Since this is Fedora-specific, the patch
# is not suitable for upstream.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/CryptoPolicies/#_cc_applications
#
# In fact, this may not be needed, since only testing code is patched.
Patch:          grpc-1.39.0-system-crypto-policies.patch
# Fix errors like:
#   TypeError: super(type, obj): obj must be an instance or subtype of type
# It is not clear why these occur.
Patch:          grpc-1.36.4-python-grpcio_tests-fixture-super.patch
# Skip tests requiring non-loopback network access when the
# FEDORA_NO_NETWORK_TESTS environment variable is set.
Patch:          grpc-1.40.0-python-grpcio_tests-make-network-tests-skippable.patch
# A handful of compression tests miss the compression ratio threshold. It seems
# to be inconsistent which particular combinations fail in a particular test
# run. It is not clear that this is a real problem. Any help in understanding
# the actual cause well enough to fix this or usefully report it upstream is
# welcome.
Patch:          grpc-1.48.0-python-grpcio_tests-skip-compression-tests.patch
# The upstream requirement to link gtest/gmock from grpc_cli is spurious.
# Remove it. We still have to build the core tests and link a test library
# (libgrpc++_test_config.so…)
Patch:          grpc-1.37.0-grpc_cli-do-not-link-gtest-gmock.patch
# Fix confusion about path to python_wrapper.sh in httpcli/httpscli tests. I
# suppose that the unpatched code must be correct for how upstream runs the
# tests, somehow.
Patch:          grpc-1.45.0-python_wrapper-path.patch
# Skip failing ChannelzServicerTest tests on Python 3.11
#
# Partially works around:
#
# grpc fails to build with Python 3.11: AttributeError: module 'inspect' has no
#   attribute 'getargspec'
# https://bugzilla.redhat.com/show_bug.cgi?id=2095027
#
# TODO: Attempt to reproduce this outside the RPM build environment and submit
# a useful/actionable upstream bug report.
Patch:          grpc-1.46.3-ChannelzServicerTest-python3.11-regressions.patch
# Running Python “test_lite”, in grpcio_tests,
# unit._dynamic_stubs_test.DynamicStubTest.test_grpc_tools_unimportable hangs.
# This may be related to:
#   [FLAKE] DynamicStubTest timeout under gevent macOS
#   https://github.com/grpc/grpc/issues/25368
# The patch simply skips the test.
Patch:          grpc-1.48.0-python-grpcio_tests-DynamicStubTest-hang.patch
# Use CMake variables for paths in pkg-config files
#
# Use @gRPC_INSTALL_LIBDIR@ for libdir; this fixes an incorrect
# -L/usr/lib on multilib Linux systems where that is the 32-bit library
# path and the correct path is /usr/lib64.
#
# Use @gRPC_INSTALL_INCLUDEDIR@ for consistency.
#
# See also:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/
#   thread/P2N35UMQVEXPILAF47RQB53MWRV2GM3J/
#
# https://github.com/grpc/grpc/pull/31671
Patch:          %{forgeurl}/pull/31671.patch
# [Test] Use ssl.SSLContext.wrap_socket, not ssl.wrap_socket
#
# The latter emits a DeprecationWarning since Python 3.10 and is removed
# in Python 3.12.
#
# https://github.com/grpc/grpc/pull/33492
#
# Backported to 1.48.4.
Patch:          grpc-1.48.4-wrap_socket.patch
# [Test] Do not use importlib find_module API, removed in Python 3.12
# https://github.com/grpc/grpc/pull/33506
#
# Backported to 1.48.4.
Patch:          grpc-1.48.4-find_module.patch
# Backport several #include directives
# These were included in https://github.com/grpc/grpc/pull/30952
#
# [Fix] Added missing #include (#34359)
# See: https://github.com/grpc/grpc/pull/34359
#
# Add abseil includes in test/cpp/end2end/xds/xds_server.h
# Downstream-only because the current release, 1.60.0, builds without changes.
#
# Together, these fix compatibility with abseil-cpp-20240116.rc1.
Patch:          grpc-1.48.4-abseil-cpp-includes.patch

# [http2] Dont drop connections on metadata limit exceeded (#32309)
#
# * [http] Dont drop connections on metadata limit exceeded
#
# * remove bad test
#
# * Automated change: Fix sanity tests
# https://github.com/grpc/grpc/commit/29d8beee0ac2555773b2a2dda5601c74a95d6c10
# https://github.com/grpc/grpc/pull/32309
#
# Fixes CVE-2023-32732
# https://nvd.nist.gov/vuln/detail/CVE-2023-32732
# CVE-2023-32732 grpc: denial of service [fedora-all]
# https://bugzilla.redhat.com/show_bug.cgi?id=2214470
#
# Backported to 1.48.4.
Patch:          0001-http2-Dont-drop-connections-on-metadata-limit-exceed.patch
# [Python] Specify noexcept for cdef functions (#34242)
#
# This is needed to build grpc with Cython 3.
#
# https://github.com/grpc/grpc/issues/33918#issuecomment-1703386656
# https://github.com/grpc/grpc/issues/33918#issuecomment-1788823585
# https://github.com/grpc/grpc/pull/34242
Patch:          0001-Specify-noexcept-for-cdef-functions.patch
# [Python] Do not call PyEval_InitThreads
# https://github.com/grpc/grpc/pull/34857
Patch:          %{forgeurl}/pull/34857.patch
# Downstream-only: work around Distribution.tests_require removal
#
# This is not suitable for offering upstream because we are so far behind
# upstream, and because it means test dependencies are no longer correctly
# generated (but the alternative is for the package not to buiild with
# setuptools 74+ at all).
Patch:          0001-Downstream-only-work-around-Distribution.tests_requi.patch

# Downstream-only patch to remove usage of coverage, per the packaging
# guidelines.  This reduces the build-time dependencies, which slightly speeds
# up builds.  It also makes this package easier port to new EPEL branches.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
Patch:          0001-Remove-usage-of-coverage.patch

# Don't include <openssl/engine.h>
# OpenSSL in Fedora provides this header in a separate openssl-devel-engine
# RPM, which is deprecated and subject to future removal.. RHEL10 has no
# such package, nor has this version of grpc has not caught up with the
# removal of engine and related headers.
Patch:		grpc-1.48.4-core-tsi-ssl_transport_security.cc.patch

Requires:       grpc-data = %{version}-%{release}

# Upstream https://github.com/protocolbuffers/upb does not support building
# with anything other than Bazel, and Bazel is not likely to make it into
# Fedora anytime soon due to its nightmarish collection of dependencies.
# Monitor this at https://bugzilla.redhat.com/show_bug.cgi?id=1470842.
# Therefore upb cannot be packaged for Fedora, and we must use the bundled
# copy.
#
# Note that upstream has never chosen a version, and it is not clear from which
# commit the bundled copy was taken or forked.
#
# Note also that libupb is installed in the system-wide linker path, which will
# be a problem if upb is ever packaged separately. We will cross that bridge if
# we get there.
Provides:       bundled(upb)
# The bundled upb itself bundles https://github.com/cyb70289/utf8; we follow
# upstream in styling this as “utf8_range”. It cannot reasonably be unbundled
# because the original code is not structured for distribution as a library (it
# does not even include header files). It is not clear which upstream commit
# was used.
Provides:       bundled(utf8_range)

# Regarding third_party/address_sorting: this looks a bit like a bundled
# library, but it is not. From a source file comment:
#   This is an adaptation of Android's implementation of RFC 6724 (in Android’s
#   getaddrinfo.c). It has some cosmetic differences from Android’s
#   getaddrinfo.c, but Android’s getaddrinfo.c was used as a guide or example
#   of a way to implement the RFC 6724 spec when this was written.

%description
gRPC is a modern open source high performance RPC framework that can run in any
environment. It can efficiently connect services in and across data centers
with pluggable support for load balancing, tracing, health checking and
authentication. It is also applicable in last mile of distributed computing to
connect devices, mobile applications and browsers to backend services.

The main usage scenarios:

  • Efficiently connecting polyglot services in microservices style
    architecture
  • Connecting mobile devices, browser clients to backend services
  • Generating efficient client libraries

Core Features that make it awesome:

  • Idiomatic client libraries in 10 languages
  • Highly efficient on wire and with a simple service definition framework
  • Bi-directional streaming with http/2 based transport
  • Pluggable auth, tracing, load balancing and health checking

This package provides the shared C core library.


%package data
Summary:        Data for gRPC bindings
License:        Apache-2.0
BuildArch:      noarch

Requires:       ca-certificates

%description data
Common data for gRPC bindings: currently, this contains only a symbolic link to
the system shared TLS certificates.


%package doc
Summary:        Documentation and examples for gRPC
License:        Apache-2.0
BuildArch:      noarch

Obsoletes:      python-grpcio-doc < 1.26.0-13
Provides:       python-grpcio-doc = %{version}-%{release}
Provides:       python-grpcio-admin-doc = %{version}-%{release}
Provides:       python-grpcio-csds-doc = %{version}-%{release}
Provides:       python-grpcio-channelz-doc = %{version}-%{release}
Provides:       python-grpcio-health-checking-doc = %{version}-%{release}
Provides:       python-grpcio-reflection-doc = %{version}-%{release}
Provides:       python-grpcio-status-doc = %{version}-%{release}
Provides:       python-grpcio-testing-doc = %{version}-%{release}

%description doc
Documentation and examples for gRPC, including Markdown documentation sources
for the following:

  • C (core)
    ○ API
    ○ Internals
  • C++
    ○ API
    ○ Internals
  • Objective C
    ○ API
    ○ Internals
  • Python
    ○ grpcio
    ○ grpcio_admin
    ○ grpcio_csds
    ○ grpcio_channelz
    ○ grpcio_health_checking
    ○ grpcio_reflection
    ○ grpcio_status
    ○ grpcio_testing

For rendered HTML documentation, please see https://grpc.io/docs/.


%package cpp
Summary:        C++ language bindings for gRPC
# License:        same as base package

Requires:       grpc%{?_isa} = %{version}-%{release}
Requires:       grpc-cpp%{?_isa} = %{version}-%{release}

Provides:       bundled(upb)
Provides:       bundled(utf8_range)

%description cpp
C++ language bindings for gRPC.


%package plugins
Summary:        Protocol buffers compiler plugins for gRPC
# License:        same as base package

Requires:       grpc%{?_isa} = %{version}-%{release}
Requires:       grpc-cpp%{?_isa} = %{version}-%{release}
Requires:       protobuf-compiler

Provides:       bundled(upb)
Provides:       bundled(utf8_range)

%description plugins
Plugins to the protocol buffers compiler to generate gRPC sources.


%package cli
Summary:        Command-line tool for gRPC
# License:        same as base package

Requires:       grpc%{?_isa} = %{version}-%{release}
Requires:       grpc-cpp%{?_isa} = %{version}-%{release}

Provides:       bundled(upb)
Provides:       bundled(utf8_range)

%description cli
The command line tool can do the following things:

  • Send unary rpc.
  • Attach metadata and display received metadata.
  • Handle common authentication to server.
  • Infer request/response types from server reflection result.
  • Find the request/response types from a given proto file.
  • Read proto request in text form.
  • Read request in wire form (for protobuf messages, this means serialized
    binary form).
  • Display proto response in text form.
  • Write response in wire form to a file.


%package devel
Summary:        Development files for gRPC library
# License:        same as base package
Requires:       grpc%{?_isa} = %{version}-%{release}
Requires:       grpc-cpp%{?_isa} = %{version}-%{release}
Requires:       grpc-plugins%{?_isa} = %{version}-%{release}

# grpc/impl/codegen/port_platform.h includes linux/version.h
Requires:       kernel-headers%{?_isa}
# grpcpp/impl/codegen/config_protobuf.h includes google/protobuf/…
Requires:       pkgconfig(protobuf)
# grpcpp/test/mock_stream.h includes gmock/gmock.h
Requires:       pkgconfig(gmock)
# grpcpp/impl/codegen/sync.h includes absl/synchronization/mutex.h
# grpc.pc has -labsl_[…]
Requires:       abseil-cpp-devel%{?_isa}
# grpc.pc has -lre2
Requires:       pkgconfig(re2)
# grpc.pc has -lcares
Requires:       cmake(c-ares)
# grpc.pc has -lz
Requires:       pkgconfig(zlib)

%description devel
Development headers and files for gRPC libraries (both C and C++).


%package -n python3-grpcio
Summary:        Python language bindings for gRPC
# License:        same as base package

# Note that the Python package has no runtime dependency on the base C library;
# everything it needs is linked statically. It is not practical to change this,
# and since they both come from the same source RPM, we do not need to attempt
# to do so.
Requires:       grpc-data = %{version}-%{release}

Provides:       bundled(upb)
Provides:       bundled(utf8_range)

# We no longer package these because they require python3dist(xds-protos),
# which has some issues:
#   - It provides files that overlap with several other packages, including
#     python-googleapis-common-protos, python-opencensus-proto, and
#     python-opentelemetry
#   - The PyPI release is not updated regularly, and version skew only makes
#     the above-mentioned problem of overlapping files worse.
#   - The “validate” package conflicts with one belonging to python-configobj
#     (in F38+), and it is the latter package that owns
#     https://pypi.org/project/validate/.
Obsoletes:      python3-grpcio-admin < 1.48.4-7
Obsoletes:      python3-grpcio-csds < 1.48.4-7

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc

%description -n python3-grpcio
Python language bindings for gRPC (HTTP/2-based RPC framework).


%global grpcio_egg %{python3_sitearch}/grpcio-%{pyversion}-py%{python3_version}.egg-info
%{?python_extras_subpkg:%python_extras_subpkg -n python3-grpcio -i %{grpcio_egg} protobuf}


%package -n python3-grpcio-tools
Summary:       Package for gRPC Python tools
# License:        same as base package

Provides:       bundled(upb)
Provides:       bundled(utf8_range)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc-tools

%description -n python3-grpcio-tools
Package for gRPC Python tools.


%package -n python3-grpcio-channelz
Summary:        Channel Level Live Debug Information Service for gRPC
License:        Apache-2.0

BuildArch:      noarch

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc-channelz

%description -n python3-grpcio-channelz
gRPC Python Channelz package
============================

Channelz is a live debug tool in gRPC Python.


%package -n python3-grpcio-health-checking
Summary:        Standard Health Checking Service for gRPC
License:        Apache-2.0

BuildArch:      noarch

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc-health

%description -n python3-grpcio-health-checking
gRPC Python Health Checking
===========================

Reference package for GRPC Python health checking.


%package -n python3-grpcio-reflection
Summary:        Standard Protobuf Reflection Service for gRPC
License:        Apache-2.0

BuildArch:      noarch

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc-reflection

%description -n python3-grpcio-reflection
gRPC Python Reflection package
==============================

Reference package for reflection in GRPC Python.


%package -n python3-grpcio-status
Summary:        Status proto mapping for gRPC
License:        Apache-2.0

BuildArch:      noarch

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc-status

%description -n python3-grpcio-status
gRPC Python Status Proto
===========================

Reference package for GRPC Python status proto mapping.


%package -n python3-grpcio-testing
Summary:        Testing utilities for gRPC Python
License:        Apache-2.0

BuildArch:      noarch

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_provides_for_importable_modules
%py_provides python3-grpc-testing

%description -n python3-grpcio-testing
gRPC Python Testing Package
===========================

Testing utilities for gRPC Python.


%prep
%autosetup -p1 -n grpc-%{srcversion}

cp -p third_party/upb/third_party/utf8_range/LICENSE LICENSE-utf8_range

echo '===== Patching grpcio_tools for system protobuf =====' 2>&1
# Build python3-grpcio_tools against system protobuf packages instead of
# expecting a git submodule. Must also add requisite linker flags using
# GRPC_PYTHON_LDFLAGS. This was formerly done by
# grpc-VERSION-python-grpcio_tools-use-system-protobuf.patch, but it had to be
# tediously but trivially rebased every patch release as the CC_FILES list
# changed, so we automated the patch.
sed -r -i \
    -e "s/^(# AUTO-GENERATED .*)/\\1\\n\
# Then, modified by hand to build with an external system protobuf\
# installation./" \
    -e 's/^(CC_FILES=\[).*(\])/\1\2/' \
    -e "s@^((CC|PROTO)_INCLUDE=')[^']+'@\1%{_includedir}'@" \
    -e '/^PROTOBUF_SUBMODULE_VERSION=/d' \
    'tools/distrib/python/grpcio_tools/protoc_lib_deps.py'

echo '===== Preparing gtest/gmock =====' 2>&1
%if %{without system_gtest}
# Copy in the needed gtest/gmock implementations.
%setup -q -T -D -b 1 -n grpc-%{srcversion}
rm -rvf 'third_party/googletest'
mv '../%{gtest_dir}' 'third_party/googletest'
%else
# Patch CMakeLists for external gtest/gmock.
#
#  1. Create dummy sources, adding a typedef so the translation unit is not
#     empty, rather than removing references to these sources from
#     CMakeLists.txt. This is so that we do not end up with executables with no
#     sources, only libraries, which is a CMake error.
#  2. Either remove references to the corresponding include directories, or
#     create the directories and leave them empty.
#  3. “Stuff” the external library into the target_link_libraries() for each
#     test by noting that GMock/GTest/GFlags are always used together.
for gwhat in test mock
do
  mkdir -p "third_party/googletest/google${gwhat}/src" \
      "third_party/googletest/google${gwhat}/include"
  echo "typedef int dummy_${gwhat}_type;" \
      > "third_party/googletest/google${gwhat}/src/g${gwhat}-all.cc"
done
sed -r -i 's/^([[:blank:]]*)(\$\{_gRPC_GFLAGS_LIBRARIES\})/'\
'\1\2\n\1gtest\n\1gmock/' CMakeLists.txt
%endif

# Extract the source tarballs needed for their .proto files, which upstream
# expects to download at build time.
%setup -q -T -D -b 2 -n grpc-%{srcversion}
%setup -q -T -D -b 3 -n grpc-%{srcversion}
%setup -q -T -D -b 4 -n grpc-%{srcversion}
%setup -q -T -D -b 5 -n grpc-%{srcversion}
{
  awk '$1 ~ /^(#|$)/ { next }; 1' <<'EOF'
../%{envoy_api_dir}/ third_party/envoy-api/
../%{googleapis_dir}/ third_party/googleapis/
../%{opencensus_proto_dir}/ third_party/opencensus-proto/
../%{xds_dir}/ third_party/xds/
EOF
} | while read -r fromdir todir
do
  # Remove everything from the external source tree except the .proto files, to
  # prove that none of it is bundled.
  find "${fromdir}" -type f ! -name '*.proto' -print -delete
  # Remove the empty directory corresponding to the git submodule
  rm -rvf "${todir}"
  # Move the extracted source, to the location where the git submodule would be
  # in a git checkout that included it.
  mv "${fromdir}" "${todir}"
done

echo '===== Removing bundled xxhash =====' 2>&1
# Remove bundled xxhash
rm -rvf third_party/xxhash
# Since grpc sets XXH_INCLUDE_ALL wherever it uses xxhash, it is using xxhash
# as a header-only library. This means we can replace it with the system copy
# by doing nothing further; xxhash.h is in the system include path and will be
# found instead, and there are no linker flags to add. See also
# https://github.com/grpc/grpc/issues/25945.

echo '===== Fixing permissions =====' 2>&1
# https://github.com/grpc/grpc/pull/27069
find . -type f -perm /0111 \
    -exec gawk '!/^#!/ { print FILENAME }; { nextfile }' '{}' '+' |
  xargs -r chmod -v a-x

echo '===== Removing selected unused sources =====' 2>&1
# Remove unused sources that have licenses not in the License field, to ensure
# they are not accidentally used in the build. See the comment above the base
# package License field for more details.
rm -rfv \
    src/boringssl/boringssl_prefix_symbols.h \
    third_party/cares/ares_build.h \
    third_party/upb/third_party/lunit
# Since we are replacing roots.pem with a symlink to the shared system
# certificates, we do not include its license (MPLv2.0) in any License field.
# We remove its contents so that, if we make a packaging mistake, we will have
# a bug but not an incorrect License field.
echo '' > etc/roots.pem

# Remove Android sources and examples. We do not need these on Linux, and they
# have some issues that will be flagged when reviewing the package, such as:
#   - Another copy of the MPLv2.0-licensed certificate bundle from
#     etc/roots.pem, in src/android/test/interop/app/src/main/assets/roots.pem
#   - Pre-built jar files at
#     src/android/test/interop/gradle/wrapper/gradle-wrapper.jar and
#     examples/android/helloworld/gradle/wrapper/gradle-wrapper.jar
rm -rvf examples/android src/android

# Drop the NodeJS example’s package-lock.json file, which will hopefully keep
# us from having bugs filed due to CVE’s in its (unpackaged) recursive
# dependencies.
rm -vf examples/node/package-lock.json

# Remove unwanted .gitignore files, generally in examples. One could argue that
# a sample .gitignore file is part of the example, but, well, we’re not going
# to do that.
find . -type f -name .gitignore -print -delete

echo '===== Fixing shebangs =====' 2>&1
# Find executables with /usr/bin/env shebangs in the examples, and fix them.
find . -type f -perm /0111 -exec gawk \
    '/^#!\/usr\/bin\/env[[:blank:]]/ { print FILENAME }; { nextfile }' \
    '{}' '+' |
  xargs -r sed -r -i '1{s|^(#!/usr/bin/)env[[:blank:]]+([^[:blank:]]+)|\1\2|}'

echo '===== Fixing hard-coded C++ standard =====' 2>&1
# We need to adjust the C++ standard to avoid abseil-related linker errors. For
# the main C++ build, we can use CMAKE_CXX_STANDARD. For extensions, examples,
# etc., we must patch.
sed -r -i 's/(std=c\+\+)14/\1%{cpp_std}/g' \
    setup.py grpc.gyp Rakefile \
    examples/cpp/*/Makefile \
    examples/cpp/*/CMakeLists.txt \
    tools/run_tests/artifacts/artifact_targets.py \
    tools/distrib/python/grpcio_tools/setup.py


%build
# ~~~~ C (core) and C++ (cpp) ~~~~

# Length of the prefix (e.g. /usr), plus a trailing slash (or newline), plus
# one, to get the index of the first relative path character after the prefix.
# This is needed because gRPC_INSTALL_*DIR options expect paths relative to the
# prefix, and supplying absolute paths causes certain subtle problems.
%global rmprefix %(echo $(($(wc -c <<<'%{_prefix}')+1)))

echo '===== Building C (core) and C++ components =====' 2>&1
# We could use either make or ninja as the backend; ninja is faster and has no
# disadvantages (except a small additional BR, given we already need Python)
#
# We need to adjust the C++ standard to avoid abseil-related linker errors.
%cmake \
    -DgRPC_INSTALL:BOOL=ON \
    -DCMAKE_CXX_STANDARD:STRING=%{cpp_std} \
    -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON \
    -DgRPC_INSTALL_BINDIR:PATH=%(cut -b %{rmprefix}- <<<'%{_bindir}') \
    -DgRPC_INSTALL_LIBDIR:PATH=%(cut -b %{rmprefix}- <<<'%{_libdir}') \
    -DgRPC_INSTALL_INCLUDEDIR:PATH=%(cut -b %{rmprefix}- <<<'%{_includedir}') \
    -DgRPC_INSTALL_CMAKEDIR:PATH=%(cut -b %{rmprefix}- <<<'%{_libdir}/cmake/grpc') \
    -DgRPC_INSTALL_SHAREDIR:PATH=%(cut -b %{rmprefix}- <<<'%{_datadir}/grpc') \
    -DgRPC_BUILD_TESTS:BOOL=%{?with_core_tests:ON}%{?!with_core_tests:OFF} \
    -DgRPC_BUILD_CODEGEN:BOOL=ON \
    -DgRPC_BUILD_CSHARP_EXT:BOOL=ON \
    -DgRPC_BACKWARDS_COMPATIBILITY_MODE:BOOL=OFF \
    -DgRPC_ZLIB_PROVIDER:STRING='package' \
    -DgRPC_CARES_PROVIDER:STRING='package' \
    -DgRPC_RE2_PROVIDER:STRING='package' \
    -DgRPC_SSL_PROVIDER:STRING='package' \
    -DgRPC_PROTOBUF_PROVIDER:STRING='package' \
    -DgRPC_PROTOBUF_PACKAGE_TYPE:STRING='MODULE' \
    -DgRPC_BENCHMARK_PROVIDER:STRING='package' \
    -DgRPC_ABSL_PROVIDER:STRING='package' \
    -DgRPC_USE_PROTO_LITE:BOOL=OFF \
    -DgRPC_BUILD_GRPC_CPP_PLUGIN:BOOL=ON \
    -DgRPC_BUILD_GRPC_CSHARP_PLUGIN:BOOL=ON \
    -DgRPC_BUILD_GRPC_NODE_PLUGIN:BOOL=ON \
    -DgRPC_BUILD_GRPC_OBJECTIVE_C_PLUGIN:BOOL=ON \
    -DgRPC_BUILD_GRPC_PHP_PLUGIN:BOOL=ON \
    -DgRPC_BUILD_GRPC_PYTHON_PLUGIN:BOOL=ON \
    -DgRPC_BUILD_GRPC_RUBY_PLUGIN:BOOL=ON \
    -GNinja
%cmake_build
# ~~~~ Python ~~~~

echo '===== Building Python grpcio package =====' 2>&1
# Since there are some interdependencies in the Python packages (e.g., many
# have setup_requires: grpcio-tools), we do temporary installs of built
# packages into a local directory as needed, and add it to the PYTHONPATH.
PYROOT="${PWD}/%{_vpath_builddir}/pyroot"
if [ -n "${PYTHONPATH-}" ]; then PYTHONPATH="${PYTHONPATH}:"; fi
PYTHONPATH="${PYTHONPATH-}${PYROOT}%{python3_sitelib}"
PYTHONPATH="${PYTHONPATH}:${PYROOT}%{python3_sitearch}"
export PYTHONPATH

# ~~ grpcio ~~
export GRPC_PYTHON_BUILD_WITH_CYTHON='True'
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL='True'
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB='True'
export GRPC_PYTHON_BUILD_SYSTEM_CARES='True'
export GRPC_PYTHON_BUILD_SYSTEM_RE2='True'
export GRPC_PYTHON_BUILD_SYSTEM_ABSL='True'
export GRPC_PYTHON_DISABLE_LIBC_COMPATIBILITY='True'
export GRPC_PYTHON_ENABLE_DOCUMENTATION_BUILD='False'
# Use the upstream defaults for GRPC_PYTHON_CFLAGS adn GRPC_PYTHON_LDFLAGS,
# except:
#
# - Add any flags necessary for using the system protobuf library.
# - Drop -lpthread and -lrt, since these are not needed on glibc 2.34 and
#   later.
# - Do not link libgcc statically (-static-libgcc).
#
# See also:
# https://developers.redhat.com/articles/2021/12/17/why-glibc-234-removed-libpthread
export GRPC_PYTHON_CFLAGS="$(
  pkg-config --cflags protobuf
) -std=c++%{cpp_std} -fvisibility=hidden -fno-wrapv -fno-exceptions"
export GRPC_PYTHON_LDFLAGS="$(pkg-config --libs protobuf)"
%py3_build
%{__python3} %{py_setup} %{?py_setup_args} install \
    -O1 --skip-build --root "${PYROOT}" --prefix %{_prefix}

# ~~ grpcio-tools ~~
echo '===== Building Python grpcio_tools package =====' 2>&1
pushd "tools/distrib/python/grpcio_tools/" >/dev/null
# When copying more things in here, make sure the subpackage License field
# stays correct. We need copies, not symlinks, so that the “graft” in
# MANIFEST.in works.
mkdir -p grpc_root/src
for srcdir in compiler
do
  cp -rp "../../../../src/${srcdir}" "grpc_root/src/"
done
cp -rp '../../../../include' 'grpc_root/'
# We must set GRPC_PYTHON_CFLAGS and GRPC_PYTHON_LDFLAGS again; grpcio_tools
# does not have the same default upstream flags as grpcio does, and it needs to
# link the protobuf compiler library.
export GRPC_PYTHON_CFLAGS="-fno-wrapv -frtti $(pkg-config --cflags protobuf)"
export GRPC_PYTHON_LDFLAGS="$(pkg-config --libs protobuf) -lprotoc"
%py3_build
# Remove unwanted shebang from grpc_tools.protoc source file, which will be
# installed without an executable bit:
find . -type f -name protoc.py -execdir sed -r -i '1{/^#!/d}' '{}' '+'
%{__python3} %{py_setup} %{?py_setup_args} install \
    -O1 --skip-build --root "${PYROOT}" --prefix %{_prefix}
popd >/dev/null

echo '===== Building pure-Python packages =====' 1>&2
for suffix in channelz health_checking reflection status testing tests
do
  echo "----> grpcio_${suffix} <----" 1>&2
  pushd "src/python/grpcio_${suffix}/" >/dev/null
  if ! echo "${suffix}" | grep -E "^(admin|csds)$" >/dev/null
  then
    %{__python3} %{py_setup} %{?py_setup_args} preprocess
  fi
  if ! echo "${suffix}" | grep -E "^(admin|csds|testing)$" >/dev/null
  then
    %{__python3} %{py_setup} %{?py_setup_args} build_package_protos
  fi
  %py3_build
  %{__python3} %{py_setup} %{?py_setup_args} install \
      -O1 --skip-build --root "${PYROOT}" --prefix %{_prefix}
  popd >/dev/null
done


%install
# ~~~~ C (core) and C++ (cpp) ~~~~
%cmake_install

%if %{with core_tests}
# For some reason, grpc_cli is not installed. Do it manually.
install -t '%{buildroot}%{_bindir}' -p -D '%{_vpath_builddir}/grpc_cli'
# grpc_cli build does not respect CMAKE_INSTALL_RPATH
# https://github.com/grpc/grpc/issues/25176
chrpath --delete '%{buildroot}%{_bindir}/grpc_cli'

# This library is also required for grpc_cli; it is built as part of the test
# code.
install -t '%{buildroot}%{_libdir}' -p \
    '%{_vpath_builddir}/libgrpc++_test_config.so.%{cpp_so_version}'
chrpath --delete \
    '%{buildroot}%{_libdir}/libgrpc++_test_config.so.%{cpp_so_version}'

install -d '%{buildroot}/%{_mandir}/man1'
install -t '%{buildroot}/%{_mandir}/man1' -p -m 0644 \
    %{SOURCE100} %{SOURCE101} %{SOURCE102} %{SOURCE103} %{SOURCE104} \
    %{SOURCE106} %{SOURCE107} %{SOURCE108}
%endif

# Remove any static libraries that may have been installed against our wishes
find %{buildroot} -type f -name '*.a' -print -delete
# Fix wrong permissions on installed headers
find %{buildroot}%{_includedir}/grpc* -type f -name '*.h' -perm /0111 \
    -execdir chmod -v a-x '{}' '+'

# ~~~~ Python ~~~~

# Since several packages have an install_requires: grpcio-tools, we must ensure
# the buildroot Python site-packages directories are in the PYTHONPATH.
pushd '%{buildroot}'
PYROOT="${PWD}"
popd
if [ -n "${PYTHONPATH-}" ]; then PYTHONPATH="${PYTHONPATH}:"; fi
PYTHONPATH="${PYTHONPATH-}${PYROOT}%{python3_sitelib}"
PYTHONPATH="${PYTHONPATH}:${PYROOT}%{python3_sitearch}"
export PYTHONPATH

# ~~ grpcio ~~
%py3_install

# ~~ grpcio-tools ~~
pushd "tools/distrib/python/grpcio_tools/" >/dev/null
%py3_install
popd >/dev/null

# ~~ pure-python modules grpcio-* ~~
for suffix in channelz health_checking reflection status testing
do
  pushd "src/python/grpcio_${suffix}/" >/dev/null
  %py3_install
  popd >/dev/null
done
# The grpcio_tests package should not be installed; it would provide top-level
# packages with generic names like “tests” or “tests_aio”.

# ~~~~ Miscellaneous ~~~~

# Replace copies of the certificate bundle with symlinks to the shared system
# certificates. This has the following benefits:
#   - Reduces duplication and save space
#   - Respects system-wide administrative trust configuration
#   - Keeps “MPLv2.0” from having to be added to a number of License fields
%global sysbundle /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem
# We do not own this file; we temporarily install it in the buildroot so we do
# not have dangling symlinks.
install -D -t "%{buildroot}$(dirname '%{sysbundle}')" -m 0644 '%{sysbundle}'

find '%{buildroot}' -type f -name 'roots.pem' |
  while read -r fn
  do
    ln -s -f "%{buildroot}%{sysbundle}" "${fn}"
    symlinks -c -o "${fn}"
  done

rm -rvf "%{buildroot}$(dirname '%{sysbundle}')"

# ~~ documentation and examples ~~

install -D -t '%{buildroot}%{_pkgdocdir}' -m 0644 -p \
    AUTHORS \
    CONCEPTS.md \
    MAINTAINERS.md \
    README.md \
    SECURITY.md \
    TROUBLESHOOTING.md
cp -rvp doc examples '%{buildroot}%{_pkgdocdir}'
# Hardlink duplicate files in the examples
hardlink -v '%{buildroot}%{_pkgdocdir}/examples/'


%check
%ifarch %{ix86}

cat <<'EOF'
Since the following changes are accepted for F37:

https://fedoraproject.org/wiki/Changes/RetireARMv7
https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval

…we still build for i686 since this is not a leaf packages, but skip tests so
we do not have to keep track of 32-bit-specific issues.
EOF

%else

export FEDORA_NO_NETWORK_TESTS=1

%if %{with core_tests}
PORT_SERVER_PORT="$(awk '
  /_PORT_SERVER_PORT[[:blank:]]*=[[:blank:]]*[[:digit:]]+$/ { print $NF }
' tools/run_tests/python_utils/start_port_server.py)"

# Note that no tests are actually found by ctest:
%ctest

# Exclude tests that are known to hang or otherwise fail. Assistance welcome in
# figuring out what is wrong with these.  Note, however, that we are running
# the tests very differently from upstream, which uses scripts in
# tools/run_tests/ that rebuild the entire source and use Docker, so it is
# likely to be difficult to get help from upstream for any failures here. Note
# that some of these tests would never work in an environment without Internet
# access.
{ sed -r -e '/^(#|$)/d' -e 's|^(.*)$|%{_vpath_builddir}/\1_test|' <<'EOF'

# Requires (or may require) network:
resolve_address_using_ares_resolver
resolve_address_using_ares_resolver_posix
resolve_address_using_native_resolver
resolve_address_using_native_resolver_posix
ssl_transport_security

# Seems to require privilege:
flaky_network

%ifarch s390x
# Unexplained:
#
# [ RUN      ] AddressSortingTest.TestSorterKnowsIpv6LoopbackIsAvailable
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/naming/address_sorting_test.cc:827: Failure
# Expected equality of these values:
#   source_addr_output->sin6_family
#     Which is: 0
#   10
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/naming/address_sorting_test.cc:837: Failure
# Expected equality of these values:
#   source_addr_str
#     Which is: "::"
#   "::1"
# [  FAILED  ] AddressSortingTest.TestSorterKnowsIpv6LoopbackIsAvailable (1 ms)
#
# Confirmed in 1.48.1 2022-09-13, possibly flaky
address_sorting
%endif

%ifarch s390x
# Unexplained:
#
# Status is not ok: Setting authenticated associated data failed
# E0912 22:53:27.561134727   29675 aes_gcm_test.cc:77]         assertion failed: status == GRPC_STATUS_OK
# *** SIGABRT received at time=1663023207 on cpu 1 ***
# PC: @      0x3ffb381cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ffb3702560  (unknown)  (unknown)
#     @      0x3ffb3702802  (unknown)  (unknown)
#     @      0x3ffb44fe490  (unknown)  (unknown)
#     @      0x3ffb381cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ffb37c9d20  (unknown)  gsignal
#     @      0x3ffb37ab364  (unknown)  abort
#     @      0x2aa26304a28  (unknown)  gsec_assert_ok()
#     @      0x2aa26304b54  (unknown)  gsec_test_random_encrypt_decrypt()
#     @      0x2aa26302536  (unknown)  main
#     @      0x3ffb37ab618  (unknown)  __libc_start_call_main
#     @      0x3ffb37ab700  (unknown)  __libc_start_main@GLIBC_2.2
#     @      0x2aa263036f0  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-12
alts_crypt
%endif

%ifarch s390x
# Unexplained:
#
# (aborted without output)
#
# Confirmed in 1.48.1 2022-09-12
alts_crypter
%endif

%ifarch s390x
# Unexplained:
#
# [ RUN      ] AltsConcurrentConnectivityTest.TestBasicClientServerHandshakes
# E0912 22:58:34.364900111   29674 alts_grpc_privacy_integrity_record_protocol.cc:107] Failed to unprotect, More bytes written than expected. Frame decryption failed.
# [… 11 similar lines omitted …]
# /builddir/build/BUILD/grpc-1.48.1/test/core/tsi/alts/handshaker/alts_concurrent_connectivity_test.cc:244: Failure
# Expected equality of these values:
#   ev.type
#     Which is: 1
#   GRPC_OP_COMPLETE
#     Which is: 2
# connect_loop runner:0x3ffc817e2f8 got ev.type:1 i:0
# [  FAILED  ] AltsConcurrentConnectivityTest.TestBasicClientServerHandshakes (5016 ms)
# [ RUN      ] AltsConcurrentConnectivityTest.TestConcurrentClientServerHandshakes
# E0912 22:58:39.512378993   29762 alts_grpc_privacy_integrity_record_protocol.cc:107] Failed to unprotect, More bytes written than expected. Frame decryption failed.
# [… 1015 similar lines omitted …]
# /builddir/build/BUILD/grpc-1.48.1/test/core/tsi/alts/handshaker/alts_concurrent_connectivity_test.cc:244: Failure
# Expected equality of these values:
#   ev.type
#     Which is: 1
#   GRPC_OP_COMPLETE
#     Which is: 2
# connect_loop runner:0x2aa1c0a7f40 got ev.type:1 i:0
# [… 28 similar 7-line groups omitted …]
# E0912 22:58:54.393525915   30129 alts_grpc_privacy_integrity_record_protocol.cc:107] Failed to unprotect, More bytes written than expected. Frame decryption failed.
# E0912 22:58:54.393664601   30143 alts_grpc_privacy_integrity_record_protocol.cc:107] Failed to unprotect, More bytes written than expected. Frame decryption failed.
# /builddir/build/BUILD/grpc-1.48.1/test/core/tsi/alts/handshaker/alts_concurrent_connectivity_test.cc:244: Failure
# Expected equality of these values:
#   ev.type
#     Which is: 1
#   GRPC_OP_COMPLETE
#     Which is: 2
# connect_loop runner:0x2aa1c0acbe0 got ev.type:1 i:0
# [… 19 similar 7-line groups omitted …]
# E0912 22:58:54.401378896   30129 alts_grpc_privacy_integrity_record_protocol.cc:107] Failed to unprotect, More bytes written than expected. Frame decryption failed.
# E0912 22:58:54.401549994   30143 alts_grpc_privacy_integrity_record_protocol.cc:107] Failed to unprotect, More bytes written than expected. Frame decryption failed.
# /builddir/build/BUILD/grpc-1.48.1/test/core/tsi/alts/handshaker/alts_concurrent_connectivity_test.cc:244: Failure
# Expected equality of these values:
#   ev.type
#     Which is: 1
#   GRPC_OP_COMPLETE
#     Which is: 2
# connect_loop runner:0x2aa1c0a8650 got ev.type:1 i:0
# [  FAILED  ] AltsConcurrentConnectivityTest.TestConcurrentClientServerHandshakes (15056 ms)
# [ RUN      ] AltsConcurrentConnectivityTest.TestHandshakeFailsFastWhenPeerEndpointClosesConnectionAfterAccepting
# [       OK ] AltsConcurrentConnectivityTest.TestHandshakeFailsFastWhenPeerEndpointClosesConnectionAfterAccepting (3080 ms)
# [ RUN      ] AltsConcurrentConnectivityTest.TestHandshakeFailsFastWhenHandshakeServerClosesConnectionAfterAccepting
# E0912 22:58:57.502419569   30351 alts_handshaker_client.cc:223] recv_buffer is nullptr in alts_tsi_handshaker_handle_response()
# [… 160 similar lines omitted …]
# [       OK ] AltsConcurrentConnectivityTest.TestHandshakeFailsFastWhenHandshakeServerClosesConnectionAfterAccepting (1199 ms)
# [ RUN      ] AltsConcurrentConnectivityTest.TestHandshakeFailsFastWhenHandshakeServerHangsAfterAccepting
# [       OK ] AltsConcurrentConnectivityTest.TestHandshakeFailsFastWhenHandshakeServerHangsAfterAccepting (308 ms)
# [----------] 5 tests from AltsConcurrentConnectivityTest (24661 ms total)
# [----------] Global test environment tear-down
# [==========] 5 tests from 1 test suite ran. (24661 ms total)
# [  PASSED  ] 3 tests.
# [  FAILED  ] 2 tests, listed below:
# [  FAILED  ] AltsConcurrentConnectivityTest.TestBasicClientServerHandshakes
# [  FAILED  ] AltsConcurrentConnectivityTest.TestConcurrentClientServerHandshakes
#  2 FAILED TESTS
# E0912 22:59:08.997892504   29669 test_config.cc:175]         Timeout in waiting for gRPC shutdown
#
# Confirmed in 1.48.1 2022-09-12
alts_concurrent_connectivity
%endif

%ifarch s390x
# Unexplained:
#
# (aborted without output)
#
# Confirmed in 1.48.1 2022-09-12
alts_frame_protector
%endif

%ifarch s390x
# Unexplained:
#
# E0914 15:16:37.948845070   29676 alts_grpc_integrity_only_record_protocol.cc:109] Failed to protect, Setting authenticated associated data failed
# E0914 15:16:37.949063396   29676 alts_grpc_record_protocol_test.cc:283] assertion failed: status == TSI_OK
# *** SIGABRT received at time=1663168597 on cpu 2 ***
# PC: @      0x3ff8da1cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ff8d902560  (unknown)  (unknown)
#     @      0x3ff8d902802  (unknown)  (unknown)
#     @      0x3ff8e77e490  (unknown)  (unknown)
#     @      0x3ff8da1cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ff8d9c9d20  (unknown)  gsignal
#     @      0x3ff8d9ab364  (unknown)  abort
#     @      0x2aa2f28375e  (unknown)  random_seal_unseal()
#     @      0x2aa2f284008  (unknown)  alts_grpc_record_protocol_tests()
#     @      0x2aa2f28258c  (unknown)  main
#     @      0x3ff8d9ab618  (unknown)  __libc_start_call_main
#     @      0x3ff8d9ab700  (unknown)  __libc_start_main@GLIBC_2.2
#     @      0x2aa2f282680  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-14
alts_grpc_record_protocol
%endif

%ifarch s390x
# Unexplained:
#
# (aborted without output)
#
# Confirmed in 1.48.1 2022-09-14
alts_iovec_record_protocol
%endif

%ifarch s390x
# Unexplained:
#
# E0914 15:23:44.474978044   29723 alts_grpc_integrity_only_record_protocol.cc:109] Failed to protect, Setting authenticated associated data failed
# E0914 15:23:44.475141948   29723 alts_zero_copy_grpc_protector_test.cc:186] assertion failed: tsi_zero_copy_grpc_protector_protect( sender, &var->original_sb, &var->protected_sb) == TSI_OK
# *** SIGABRT received at time=1663169024 on cpu 0 ***
# PC: @      0x3ff9079cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ff90682560  (unknown)  (unknown)
#     @      0x3ff90682802  (unknown)  (unknown)
#     @      0x3ff914fe490  (unknown)  (unknown)
#     @      0x3ff9079cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ff90749d20  (unknown)  gsignal
#     @      0x3ff9072b364  (unknown)  abort
#     @      0x2aa01c83324  (unknown)  seal_unseal_small_buffer()
#     @      0x2aa01c83538  (unknown)  alts_zero_copy_protector_seal_unseal_small_buffer_tests()
#     @      0x2aa01c8254a  (unknown)  main
#     @      0x3ff9072b618  (unknown)  __libc_start_call_main
#     @      0x3ff9072b700  (unknown)  __libc_start_main@GLIBC_2.2
#     @      0x2aa01c82630  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-14
alts_zero_copy_grpc_protector
%endif

# Unexplained, flaky:
#
# (hangs indefinitely, timeout triggered)
#
# Confirmed in 1.48.1 2022-09-13
client_ssl

%ifarch s390x riscv64
# Unexplained:
#
# [ RUN      ] CredentialsTest.TestOauth2TokenFetcherCredsParsingEmptyHttpBody
# E0907 14:32:31.499040041   70130 oauth2_credentials.cc:177]  Call to http server ended with error 401 [{"access_token":"ya29.AHES6ZRN3-HlhAPya30GnW_bHSb_", "expires_in":3599,  "token_type":"Bearer"}].
# *** SIGSEGV received at time=1662561151 on cpu 2 ***
# PC: @      0x3ffb434b8c8  (unknown)  grpc_oauth2_token_fetcher_credentials_parse_server_response()
#     @      0x3ffb3102560  (unknown)  (unknown)
#     @      0x3ffb3102802  (unknown)  (unknown)
#     @      0x3ffb467e490  (unknown)  (unknown)
#     @      0x3ffb434b8c8  (unknown)  grpc_oauth2_token_fetcher_credentials_parse_server_response()
#     @      0x2aa1f82c360  (unknown)  grpc_core::(anonymous namespace)::CredentialsTest_TestOauth2TokenFetcherCredsParsingEmptyHttpBody_Test::TestBody()
#     @      0x2aa1f890e76  (unknown)  testing::internal::HandleExceptionsInMethodIfSupported<>()
#     @      0x2aa1f87af2a  (unknown)  testing::Test::Run()
#     @      0x2aa1f87b1fe  (unknown)  testing::TestInfo::Run()
#     @      0x2aa1f87b420  (unknown)  testing::TestSuite::Run()
#     @      0x2aa1f884936  (unknown)  testing::internal::UnitTestImpl::RunAllTests()
#     @      0x2aa1f891406  (unknown)  testing::internal::HandleExceptionsInMethodIfSupported<>()
#     @      0x2aa1f87b706  (unknown)  testing::UnitTest::Run()
#     @      0x2aa1f81e96e  (unknown)  main
#     @      0x3ffb31ab618  (unknown)  __libc_start_call_main
#     @      0x3ffb31ab700  (unknown)  __libc_start_main@GLIBC_2.2
#     @      0x2aa1f823d80  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-07
test_core_security_credentials
%endif

%ifarch x86_64 aarch64
# Unexplained:
#
# [ RUN      ] ExamineStackTest.AbseilStackProvider
# /builddir/build/BUILD/grpc-1.48.1/test/core/gprpp/examine_stack_test.cc:75: Failure
# Value of: stack_trace->find("GetCurrentStackTrace") != std::string::npos
#   Actual: false
# Expected: true
# [  FAILED  ] ExamineStackTest.AbseilStackProvider (0 ms)
#
# Confirmed in 1.48.1 2022-09-13
examine_stack
%endif

%ifarch s390x
# Unexplained:
#
# E0914 18:50:00.139725989   58193 cq_verifier.cc:228]         no event received, but expected:tag(257) GRPC_OP_COMPLETE success=1 /builddir/build/BUILD/grpc-1.48.1/test/core/end2end/goaway_server_test.cc:271
# tag(769) GRPC_OP_COMPLETE success=1 /builddir/build/BUILD/grpc-1.48.1/test/core/end2end/goaway_server_test.cc:272
# *** SIGABRT received at time=1663181400 on cpu 0 ***
# PC: @      0x3ff8bf9cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ff8be82560  (unknown)  (unknown)
#     @      0x3ff8be82802  (unknown)  (unknown)
#     @      0x3ff8cefe490  (unknown)  (unknown)
#     @      0x3ff8bf9cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ff8bf49d20  (unknown)  gsignal
#     @      0x3ff8bf2b364  (unknown)  abort
#     @      0x2aa21f05a88  (unknown)  cq_verify()
#     @      0x2aa21f03fc8  (unknown)  main
#     @      0x3ff8bf2b618  (unknown)  __libc_start_call_main
#     @      0x3ff8bf2b700  (unknown)  __libc_start_main@GLIBC_2.2
#     @      0x2aa21f04730  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-14
goaway_server
%endif

%ifarch aarch64 x86_64 ppc64le s390x riscv64
# Unexplained:
#
# [ RUN      ] GrpcToolTest.CallCommandWithTimeoutDeadlineSet
# [libprotobuf ERROR google/protobuf/text_format.cc:335] Error parsing text-format grpc.testing.SimpleRequest: 1:7: Message type "grpc.testing.SimpleRequest" has no field named "redhat".
# Failed to convert text format to proto.
# Failed to parse request.
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/util/grpc_tool_test.cc:915: Failure
# Value of: 0 == GrpcToolMainLib(ArraySize(argv), argv, TestCliCredentials(), std::bind(PrintStream, &output_stream, std::placeholders::_1))
#   Actual: false
# Expected: true
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/util/grpc_tool_test.cc:920: Failure
# Value of: nullptr != strstr(output_stream.str().c_str(), "message: \"true\"")
#   Actual: false
# Expected: true
# [  FAILED  ] GrpcToolTest.CallCommandWithTimeoutDeadlineSet (5 ms)
#
# Confirmed in 1.48.1 2022-09-14
grpc_tool
%endif

%ifarch s390x
# Unexplained:
#
# *** SIGABRT received at time=1663181750 on cpu 2 ***
# PC: @      0x3ffaec9cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ffaeb82560  (unknown)  (unknown)
#     @      0x3ffaeb82802  (unknown)  (unknown)
#     @      0x3ffaf37e490  (unknown)  (unknown)
#     @      0x3ffaec9cf2a  (unknown)  __pthread_kill_implementation
#     @      0x3ffaec49d20  (unknown)  gsignal
#     @      0x3ffaec2b364  (unknown)  abort
#     @      0x2aa1be8145e  (unknown)  verification_test()
#     @      0x2aa1be811e8  (unknown)  main
#     @      0x3ffaec2b618  (unknown)  __libc_start_call_main
#     @      0x3ffaec2b700  (unknown)  __libc_start_main@GLIBC_2.2
#     @      0x2aa1be81270  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-14
murmur_hash
%endif

%ifarch ppc64le
# Unexplained
#
# Times out at:
# [ RUN      ] RlsEnd2endTest.RlsAuthorityDeathTest
#
# Confirmed in 1.48.1 2025-02-10
rls_end2end
%endif

%ifarch ppc64le
# Times out, apparently due to an unsafe combination of death tests and
# threads:
#
# [WARNING]
# /builddir/build/BUILD/grpc-1.48.4-build/grpc-1.48.4/third_party/googletest/googletest/src/gtest-death-test.cc:1124::
# Death tests use fork(), which is unsafe particularly in a threaded context.
# For this test, Google Test detected 4 threads. See
# https://github.com/google/googletest/blob/master/docs/advanced.md#death-tests-and-threads
# for more explanation and suggested solutions, especially if this is the last
# message you see before your test times out.
#
# Confirmed in 1.48.1 2025-02-09
service_config
%endif

%ifarch x86_64 aarch64
# Unexplained:
#
# [ RUN      ] StackTracerTest.Basic
# /builddir/build/BUILD/grpc-1.48.1/test/core/util/stack_tracer_test.cc:36: Failure
# Value of: absl::StrContains(stack_trace, "Basic")
#   Actual: false
# Expected: true
# [  FAILED  ] StackTracerTest.Basic (0 ms)
#
# Confirmed in 1.48.1 2022-09-14
stack_tracer
%endif

%ifarch aarch64 x86_64 ppc64le
# Unexplained:
#
# This may be flaky and sometimes succeed; this was known to be the case on
# ppc64le in older versions.
#
# [ RUN      ] CredentialsTest.TestOauth2TokenFetcherCredsParsingEmptyHttpBody
# *** SIGSEGV received at time=1663181447 on cpu 2 ***
# PC: @     0x7fdda4098c3c  (unknown)  __strlen_evex
#     @               0x32  (unknown)  (unknown)
#
# Confirmed in 1.48.1 2022-09-14
test_core_security_credentials
%endif

%ifarch aarch64 x86_64 ppc64le s390x riscv64
# It looks like server_key_log has the right lines, but in an unexpected order.
# It is not immediately obvious if this a real problem, or an implementation
# quirk. Opinions about whether, or how, to report this upstream are welcome!
#
# [ RUN      ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_false__enable_tls_key_logging_true
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/end2end/tls_key_export_test.cc:277: Failure
# Value of: server_key_log
# Expected: is equal to "SERVER_HANDSHAKE_TRAFFIC_SECRET eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 f7d20427eda7b69db54be3032a3f1f05a0f55d1108defd15e1a2dae211dc00214554caaaac25e541e08a8a49976f2094\rEXPORTER_SECRET eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 b0b765b3d8df4388fd1232921dfe943923c971886feda8bb55673d91f90be4466d18e47305c6c84348a58d6d1f1d1d2e\rSERVER_TRAFFIC_SECRET_0 eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 58fcaf175146ac0efc4e32ed3cd73bb10e35103453ea3bf3ad11296a5902628ba692f4c06269912d94982ea56276dd6b\rCLIENT_HANDSHAKE_TRAFFIC_SECRET eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 92814e941dd4b724b0eadebdb424c029d2bd4f028cf693f72315752198a9d0ec85a68a3197570f1b7aaa1b1f200c2797\rCLIENT_TRAFFIC_SECRET_0 eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 3a9d4b7afebad9b50d7b9d71f5f508df54d90303d6beb941c5b1d8d10e19923f3928546bbe7a64c8613d5e715ff030b9\r"
#   Actual: "SERVER_HANDSHAKE_TRAFFIC_SECRET eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 f7d20427eda7b69db54be3032a3f1f05a0f55d1108defd15e1a2dae211dc00214554caaaac25e541e08a8a49976f2094\rCLIENT_HANDSHAKE_TRAFFIC_SECRET eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 92814e941dd4b724b0eadebdb424c029d2bd4f028cf693f72315752198a9d0ec85a68a3197570f1b7aaa1b1f200c2797\rEXPORTER_SECRET eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 b0b765b3d8df4388fd1232921dfe943923c971886feda8bb55673d91f90be4466d18e47305c6c84348a58d6d1f1d1d2e\rSERVER_TRAFFIC_SECRET_0 eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 58fcaf175146ac0efc4e32ed3cd73bb10e35103453ea3bf3ad11296a5902628ba692f4c06269912d94982ea56276dd6b\rCLIENT_TRAFFIC_SECRET_0 eef4f25d9d199eb0df0e2305e6d25339b85921dc6cc074fc8c20dbd6accc0203 3a9d4b7afebad9b50d7b9d71f5f508df54d90303d6beb941c5b1d8d10e19923f3928546bbe7a64c8613d5e715ff030b9\r"
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/end2end/tls_key_export_test.cc:277: Failure
# Value of: server_key_log
# Expected: is equal to "SERVER_HANDSHAKE_TRAFFIC_SECRET 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 dcd6d6638d96fe74db4bf9ac393a4b481a7d611972c21e95da4f971e6295fe60fbce33a8bdb466fe4e2a409e005259b5\rEXPORTER_SECRET 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 0637c81033fdfe3bed0b3eb3a4ea4c23246641d530fa695672d2e00aef18ebab4b25d6d38fd7a948f6a77fade9297fe7\rSERVER_TRAFFIC_SECRET_0 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 987dde02bc0757e3e9b309bf57c228c43243fe5abc2b93fa7bffa400065935d7b4e04fb709609e018fe94c71f5cd283e\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 e4badfe723bd95761bad8be436d3db2af0d4ed724cf0de092a2cad635e4bdead50a428a5e3a566c766ab92f8d2c47468\rCLIENT_TRAFFIC_SECRET_0 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 ce55a02ed58902ccf6b70df880d3314a584a686bb751cc168c4a6aa9753312c051000e8fbf01de957f2cdee41563604a\r"
#   Actual: "SERVER_HANDSHAKE_TRAFFIC_SECRET 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 dcd6d6638d96fe74db4bf9ac393a4b481a7d611972c21e95da4f971e6295fe60fbce33a8bdb466fe4e2a409e005259b5\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 e4badfe723bd95761bad8be436d3db2af0d4ed724cf0de092a2cad635e4bdead50a428a5e3a566c766ab92f8d2c47468\rEXPORTER_SECRET 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 0637c81033fdfe3bed0b3eb3a4ea4c23246641d530fa695672d2e00aef18ebab4b25d6d38fd7a948f6a77fade9297fe7\rSERVER_TRAFFIC_SECRET_0 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 987dde02bc0757e3e9b309bf57c228c43243fe5abc2b93fa7bffa400065935d7b4e04fb709609e018fe94c71f5cd283e\rCLIENT_TRAFFIC_SECRET_0 0aa0e0df58ebad99c8610573e28cdd0ea6629bc3e4eab31ec45a713e9a789ae6 ce55a02ed58902ccf6b70df880d3314a584a686bb751cc168c4a6aa9753312c051000e8fbf01de957f2cdee41563604a\r"
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/end2end/tls_key_export_test.cc:277: Failure
# Value of: server_key_log
# Expected: is equal to "SERVER_HANDSHAKE_TRAFFIC_SECRET df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 c5fc8018e0d9b3d1af85cc5fff423b8f45087ca07194ff9f3576656111c566e8bef7e3e896b75aa2fd601ad6333f0f26\rEXPORTER_SECRET df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 84233022a806f7f281cdec34cf2312b8e7101e428a84abf85c03e8478ec846a31d874dda24a7589d44c7d51610a67ea5\rSERVER_TRAFFIC_SECRET_0 df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 6463382c0cdf3d2b850419e70bffeb8c6d9bce5db1c112cae4baf2b553fc3d9a7b783ed38c2f45b0e806d5a024aaffab\rCLIENT_HANDSHAKE_TRAFFIC_SECRET df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 b55c4d1d1e72714014c3505ff3da57bd14490b299c8f6398ef6a3aba03c090c8514dc4e0b8e2e9503e59af82d793b78d\rCLIENT_TRAFFIC_SECRET_0 df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 b11c752b4e715a8b40d23791c47eace7a59c5e73080b1da04cae557a1881d01c9e3fd191d96747b2926b422c08dc87b1\r"
#   Actual: "SERVER_HANDSHAKE_TRAFFIC_SECRET df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 c5fc8018e0d9b3d1af85cc5fff423b8f45087ca07194ff9f3576656111c566e8bef7e3e896b75aa2fd601ad6333f0f26\rCLIENT_HANDSHAKE_TRAFFIC_SECRET df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 b55c4d1d1e72714014c3505ff3da57bd14490b299c8f6398ef6a3aba03c090c8514dc4e0b8e2e9503e59af82d793b78d\rEXPORTER_SECRET df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 84233022a806f7f281cdec34cf2312b8e7101e428a84abf85c03e8478ec846a31d874dda24a7589d44c7d51610a67ea5\rSERVER_TRAFFIC_SECRET_0 df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 6463382c0cdf3d2b850419e70bffeb8c6d9bce5db1c112cae4baf2b553fc3d9a7b783ed38c2f45b0e806d5a024aaffab\rCLIENT_TRAFFIC_SECRET_0 df2e54c90fc9036eb8a8565733de306f36e60067df4d83772ee8105ff7ddaea7 b11c752b4e715a8b40d23791c47eace7a59c5e73080b1da04cae557a1881d01c9e3fd191d96747b2926b422c08dc87b1\r"
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/end2end/tls_key_export_test.cc:277: Failure
# Value of: server_key_log
# Expected: is equal to "SERVER_HANDSHAKE_TRAFFIC_SECRET 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 5496b13a3e9064741476ab17e308263a9fe55e47d26f136895dc551f4ebd9d90738960e97cd1d78cb5e5326669e7d74d\rEXPORTER_SECRET 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 59f36680c801582c2c4e8f05ed2f7d838cbecdb741004d1f49377bd268cde3d317c913de38baf5fa701232a3e7c262a7\rSERVER_TRAFFIC_SECRET_0 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 0abcaad18e36929489b73a4783d41a4c52f0086923b1476ea3cfed5035ae9377b39ed9b9b51e153267f305b31610482d\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 cc36b79ed8d7986164bd4e3482239b3dabc4348f1ea1d70048ac8d1fd884dbbd0b3afbb33a17018444cba0cd739a136c\rCLIENT_TRAFFIC_SECRET_0 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 a84993ee9b9b938f68bfebf1abd703f7c7b776b9170c913c27385d0be9b133374b542bd8769e9272232894a008c45bae\r"
#   Actual: "SERVER_HANDSHAKE_TRAFFIC_SECRET 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 5496b13a3e9064741476ab17e308263a9fe55e47d26f136895dc551f4ebd9d90738960e97cd1d78cb5e5326669e7d74d\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 cc36b79ed8d7986164bd4e3482239b3dabc4348f1ea1d70048ac8d1fd884dbbd0b3afbb33a17018444cba0cd739a136c\rEXPORTER_SECRET 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 59f36680c801582c2c4e8f05ed2f7d838cbecdb741004d1f49377bd268cde3d317c913de38baf5fa701232a3e7c262a7\rSERVER_TRAFFIC_SECRET_0 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 0abcaad18e36929489b73a4783d41a4c52f0086923b1476ea3cfed5035ae9377b39ed9b9b51e153267f305b31610482d\rCLIENT_TRAFFIC_SECRET_0 28b08520f2b4f4238e78adf378efc0caea3bbf123767522d950f75da0f0c09b4 a84993ee9b9b938f68bfebf1abd703f7c7b776b9170c913c27385d0be9b133374b542bd8769e9272232894a008c45bae\r"
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/end2end/tls_key_export_test.cc:277: Failure
# Value of: server_key_log
# Expected: is equal to "SERVER_HANDSHAKE_TRAFFIC_SECRET 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 451c0c2e870b4971c2f965d75baa1ca1c5bd417aeb6d9f7fd20a45424505249c87d4b4d6437f2c4fe06e0f4652a68564\rEXPORTER_SECRET 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 fc31c6fb0afdb466c17e3cee04564f7061a553239d88b0c7a1711de757d37288814e6a27e00dbad87ef610d5460db8bd\rSERVER_TRAFFIC_SECRET_0 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 c00928d08ab817a90a9abb72b8b3caedeb7f575c917bb923635ec9b6023a4dc205275cc60cf891fe5102b4375a4823e9\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 fb6067e497dafcfeb3c8cc5183c64d560d7fd59e012f0def755eb5b54436a9d4f369dd30fc0cad8f629406520edc2116\rCLIENT_TRAFFIC_SECRET_0 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 27b3e7b94858f398a8359f332caebd571ed63e8f2c7fec489e9b33d1ed369201b308922b96d15522a75987e6634c61f3\r"
#   Actual: "SERVER_HANDSHAKE_TRAFFIC_SECRET 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 451c0c2e870b4971c2f965d75baa1ca1c5bd417aeb6d9f7fd20a45424505249c87d4b4d6437f2c4fe06e0f4652a68564\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 fb6067e497dafcfeb3c8cc5183c64d560d7fd59e012f0def755eb5b54436a9d4f369dd30fc0cad8f629406520edc2116\rEXPORTER_SECRET 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 fc31c6fb0afdb466c17e3cee04564f7061a553239d88b0c7a1711de757d37288814e6a27e00dbad87ef610d5460db8bd\rSERVER_TRAFFIC_SECRET_0 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 c00928d08ab817a90a9abb72b8b3caedeb7f575c917bb923635ec9b6023a4dc205275cc60cf891fe5102b4375a4823e9\rCLIENT_TRAFFIC_SECRET_0 5b30cc82f1b34055a02ba85fa15f08e909a2d4dfe1a07d43143e3c7df0efa250 27b3e7b94858f398a8359f332caebd571ed63e8f2c7fec489e9b33d1ed369201b308922b96d15522a75987e6634c61f3\r"
# [  FAILED  ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_false__enable_tls_key_logging_true, where GetParam() = 8-byte object <05-00 00-00 00-01 00-00> (82 ms)
# [ RUN      ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_true__enable_tls_key_logging_true
# /builddir/build/BUILD/grpc-1.48.1/test/cpp/end2end/tls_key_export_test.cc:277: Failure
# Value of: server_key_log
# Expected: is equal to "SERVER_HANDSHAKE_TRAFFIC_SECRET 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e c46a83cd4156c9f5a3c53a8d673cb888543a535fcacc6e5a0067ccf92afd7104213effe874ff31ea930210caa480cf27\rEXPORTER_SECRET 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 07b8fce3c826593d7e66527c22ebc710b4ef64f8c2921b9c89f99ebfca4df37d9852dc0f35ffc0b5046c5daee48b35d4\rSERVER_TRAFFIC_SECRET_0 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 672b3ece1a18396aa4645db0617cf4002c6ce8b039a6b522fa3a6788ec1744b3e189304a99906c24cd95298e258b54ad\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 4fc7b8e8577b8ac51e59f13acf73c8a67a15af43f4965dad6ecfd31136cc09a2b518784925e5c0bf6375f23d5e088113\rCLIENT_TRAFFIC_SECRET_0 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 20bd3408a8d1f2c779e1895c74b639631d645e1b97cf291964a0fa7b4702ad308213170e7784d47cd411d881d258b9e6\rSERVER_HANDSHAKE_TRAFFIC_SECRET 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 521a5a83ce0b115757dddfc068379813eba5ecbca8e0dc6c8211a05b029b13cb6c4acf359697a9c0b02e55bfdcf1fb57\rEXPORTER_SECRET 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 15c107ae3607293d1a245dada03d96ca3ac0b2e94447ec6bc6d5af695e54960397c431da64c04c702ea226338128067a\rSERVER_TRAFFIC_SECRET_0 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 5956d61b750355c655304d1aca8d723b15a9b29fe18609784e0b6c8d819e53cf45030669b9a51a886f3f18ca4d1b0f73\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 09045680090473c5920facdcc5849fa98b267803d0216257a0c552806073de15a73d3e47bf28374e030ed4de1ffe9be9\rCLIENT_TRAFFIC_SECRET_0 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 79f9b1819ccd9b69980c4788cd65f87b0d288835c62890234eb0fc942eede6b74a789ce9767bc3245e6363f18ac58fa6\rSERVER_HANDSHAKE_TRAFFIC_SECRET 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 f491b5d8e9c5bf4a38d12966093f8da613766d4c7dc3f557337b08e4f6b1af105527e2e46f19c4bd947b2b1b5fe3e314\rEXPORTER_SECRET 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 a2467e5c30484d3f7b3ce05be675c2465a237e1b3d772fd2745e9b181a881a8f9aaee8ae4b7980ab8c934a02c58e61a7\rSERVER_TRAFFIC_SECRET_0 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 990211d781ad8eb19cc2db122eb3868e737aa6b7143799f4b8f72a7ea672bef0e65ab6630924169c6dd2f59f55846aee\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 612f16033cc1e94849dc3a206247c5760421a94f68f2e9cde33b48e616b591d60be853f27b7537aa8f59ad4aec85e55a\rCLIENT_TRAFFIC_SECRET_0 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 2093ffbaa9b85f7cbb4d00653036f3f6986dfaec000b46add51919390b17b49e02ecb34c3be5dc48aa21e218d9d3d70f\rSERVER_HANDSHAKE_TRAFFIC_SECRET 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 3ae3754f332170315dd4516cb8f062ac5fae2afa54f6820403d22ddb2397ae30b4aa21140a68162acac270a6a71d9f51\rEXPORTER_SECRET 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 553d9efb308797f20cbfe73096082bf3c07725f0b4d0d151d1c0322aa49623a25184c9fe845069d040d6ec9f0e75f214\rSERVER_TRAFFIC_SECRET_0 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 95c9db31c38deb0c074ee7cea5e8e454ab30afea554f5d7ea5f7e91f28665d9990da2630dd55721046eb87acb3ddb335\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 54d0f425309fe118311e179d8bcd965ef696a9cacca1a78369ef10164dbc7e7418f2ceaf9cceb51033e5984aed76ef3a\rCLIENT_TRAFFIC_SECRET_0 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 9c44fcd6a41a5c3701365fbc28ddc6dd1369ddf82cbaac150995424782d2a0dc0dcf58676b88f939e403fbd5580a74bf\rSERVER_HANDSHAKE_TRAFFIC_SECRET c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 cbf5ae80e7c2d4f4d8a76bafed3a9b297ec8a35ef6ce8d1b2328afc20a73407b7e237ad100761e81e3dda1a4a7e329e1\rEXPORTER_SECRET c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 43c3d3ca25c476f8a929cc90101b91e740a54e83e31a1eb651327b7dd597a9a6d30ad62d9eae5f2de21720883fa4ab7f\rSERVER_TRAFFIC_SECRET_0 c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 26af089be6c5e54a725d099b1ddb7d2ce703dce8e84b3575d283703f690c7acce0fd775eac9abf9b2ccb04f49f6bfb1c\rCLIENT_HANDSHAKE_TRAFFIC_SECRET c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 957b72988d54b864532fe51256a59c55b69b8dfefcbbf81f4378493d0cf3b288fe111f9000c49857d35d63ea3e519d72\rCLIENT_TRAFFIC_SECRET_0 c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 62b416237b731eb435e5392baf3ae37be85c9844f9f55a7440bb74b60a2866b72b09bfaba1f6ea7b07328a38b3595808\r"
#   Actual: "SERVER_HANDSHAKE_TRAFFIC_SECRET 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e c46a83cd4156c9f5a3c53a8d673cb888543a535fcacc6e5a0067ccf92afd7104213effe874ff31ea930210caa480cf27\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 4fc7b8e8577b8ac51e59f13acf73c8a67a15af43f4965dad6ecfd31136cc09a2b518784925e5c0bf6375f23d5e088113\rEXPORTER_SECRET 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 07b8fce3c826593d7e66527c22ebc710b4ef64f8c2921b9c89f99ebfca4df37d9852dc0f35ffc0b5046c5daee48b35d4\rSERVER_TRAFFIC_SECRET_0 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 672b3ece1a18396aa4645db0617cf4002c6ce8b039a6b522fa3a6788ec1744b3e189304a99906c24cd95298e258b54ad\rCLIENT_TRAFFIC_SECRET_0 20afdda8ca612c07e6ae5036ce4cd572edf444e61112b85908b15a9ca4ac3a5e 20bd3408a8d1f2c779e1895c74b639631d645e1b97cf291964a0fa7b4702ad308213170e7784d47cd411d881d258b9e6\rSERVER_HANDSHAKE_TRAFFIC_SECRET 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 521a5a83ce0b115757dddfc068379813eba5ecbca8e0dc6c8211a05b029b13cb6c4acf359697a9c0b02e55bfdcf1fb57\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 09045680090473c5920facdcc5849fa98b267803d0216257a0c552806073de15a73d3e47bf28374e030ed4de1ffe9be9\rEXPORTER_SECRET 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 15c107ae3607293d1a245dada03d96ca3ac0b2e94447ec6bc6d5af695e54960397c431da64c04c702ea226338128067a\rSERVER_TRAFFIC_SECRET_0 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 5956d61b750355c655304d1aca8d723b15a9b29fe18609784e0b6c8d819e53cf45030669b9a51a886f3f18ca4d1b0f73\rCLIENT_TRAFFIC_SECRET_0 27174ce3e1d552c80bd1a22d2cec50f31dee027f362ff7f3bf9f5d77ba464cef 79f9b1819ccd9b69980c4788cd65f87b0d288835c62890234eb0fc942eede6b74a789ce9767bc3245e6363f18ac58fa6\rSERVER_HANDSHAKE_TRAFFIC_SECRET 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 f491b5d8e9c5bf4a38d12966093f8da613766d4c7dc3f557337b08e4f6b1af105527e2e46f19c4bd947b2b1b5fe3e314\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 612f16033cc1e94849dc3a206247c5760421a94f68f2e9cde33b48e616b591d60be853f27b7537aa8f59ad4aec85e55a\rEXPORTER_SECRET 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 a2467e5c30484d3f7b3ce05be675c2465a237e1b3d772fd2745e9b181a881a8f9aaee8ae4b7980ab8c934a02c58e61a7\rSERVER_TRAFFIC_SECRET_0 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 990211d781ad8eb19cc2db122eb3868e737aa6b7143799f4b8f72a7ea672bef0e65ab6630924169c6dd2f59f55846aee\rCLIENT_TRAFFIC_SECRET_0 37cf050f83316e6f7cb7256d5ece7b9f4c53e014bebdd9bc4393c934c5120ac9 2093ffbaa9b85f7cbb4d00653036f3f6986dfaec000b46add51919390b17b49e02ecb34c3be5dc48aa21e218d9d3d70f\rSERVER_HANDSHAKE_TRAFFIC_SECRET 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 3ae3754f332170315dd4516cb8f062ac5fae2afa54f6820403d22ddb2397ae30b4aa21140a68162acac270a6a71d9f51\rCLIENT_HANDSHAKE_TRAFFIC_SECRET 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 54d0f425309fe118311e179d8bcd965ef696a9cacca1a78369ef10164dbc7e7418f2ceaf9cceb51033e5984aed76ef3a\rEXPORTER_SECRET 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 553d9efb308797f20cbfe73096082bf3c07725f0b4d0d151d1c0322aa49623a25184c9fe845069d040d6ec9f0e75f214\rSERVER_TRAFFIC_SECRET_0 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 95c9db31c38deb0c074ee7cea5e8e454ab30afea554f5d7ea5f7e91f28665d9990da2630dd55721046eb87acb3ddb335\rCLIENT_TRAFFIC_SECRET_0 034d3800864d87141abc05a3e17e84726ce10b85d931eb5d00eadd80984dbb7e 9c44fcd6a41a5c3701365fbc28ddc6dd1369ddf82cbaac150995424782d2a0dc0dcf58676b88f939e403fbd5580a74bf\rSERVER_HANDSHAKE_TRAFFIC_SECRET c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 cbf5ae80e7c2d4f4d8a76bafed3a9b297ec8a35ef6ce8d1b2328afc20a73407b7e237ad100761e81e3dda1a4a7e329e1\rCLIENT_HANDSHAKE_TRAFFIC_SECRET c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 957b72988d54b864532fe51256a59c55b69b8dfefcbbf81f4378493d0cf3b288fe111f9000c49857d35d63ea3e519d72\rEXPORTER_SECRET c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 43c3d3ca25c476f8a929cc90101b91e740a54e83e31a1eb651327b7dd597a9a6d30ad62d9eae5f2de21720883fa4ab7f\rSERVER_TRAFFIC_SECRET_0 c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 26af089be6c5e54a725d099b1ddb7d2ce703dce8e84b3575d283703f690c7acce0fd775eac9abf9b2ccb04f49f6bfb1c\rCLIENT_TRAFFIC_SECRET_0 c98b2b143864bb78bfb7bac233c1e4bb463eb7bbfe18ed056293e4d8752596c9 62b416237b731eb435e5392baf3ae37be85c9844f9f55a7440bb74b60a2866b72b09bfaba1f6ea7b07328a38b3595808\r"
# [  FAILED  ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_true__enable_tls_key_logging_true, where GetParam() = 8-byte object <05-00 00-00 01-01 00-00> (69 ms)
# [ RUN      ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_true__enable_tls_key_logging_false
# [       OK ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_true__enable_tls_key_logging_false (64 ms)
# [ RUN      ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_false__enable_tls_key_logging_false
# [       OK ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_false__enable_tls_key_logging_false (66 ms)
# [----------] 4 tests from TlsKeyLogging/TlsKeyLoggingEnd2EndTest (284 ms total)
# [----------] Global test environment tear-down
# [==========] 4 tests from 1 test suite ran. (284 ms total)
# [  PASSED  ] 2 tests.
# [  FAILED  ] 2 tests, listed below:
# [  FAILED  ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_false__enable_tls_key_logging_true, where GetParam() = 8-byte object <05-00 00-00 00-01 00-00>
# [  FAILED  ] TlsKeyLogging/TlsKeyLoggingEnd2EndTest.KeyLogging/TestScenario__num_listening_ports_5__share_tls_key_log_file_true__enable_tls_key_logging_true, where GetParam() = 8-byte object <05-00 00-00 01-01 00-00>
# 2 FAILED TESTS
#
# Confirmed in 1.48.1 2022-09-15
tls_key_export
%endif

EOF
} | xargs -r chmod -v a-x

find %{_vpath_builddir} -type f -perm /0111 -name '*_test' | sort |
  while read -r testexe
  do
    echo "==== $(date -u --iso-8601=ns): $(basename "${testexe}") ===="
    %{__python3} tools/run_tests/start_port_server.py

%if %{without gdb}
    # There is a history of some tests failing by hanging. We use “timeout” so
    # that a test that does hang breaks the build in a vagurely reasonable
    # amount of time. Some tests really can be slow, so the timeout is long!
    timeout -k 61m -v 60m \
%if %{with valgrind}
        valgrind --trace-children=yes --leak-check=full --track-origins=yes \
%endif
        "${testexe}"
%else
    # Script gdb to run the test file and record any backtrace. Note that this
    # reports an error when tests fail, because there is no stack on which to
    # report a backtrace after the test exits successfully, and that this keeps
    # going after a test fails, because we ignore the mentioned error. A
    # cleverer gdb script would be nice, but this is good enough for the
    # intended purpose.
    tee "${testexe}-script.gdb" <<EOF
set pagination off
set logging file ${testexe}-gdb.log
set logging on
file ${testexe}
run
bt -full
set logging off
quit
EOF
    gdb -q -x "${testexe}-script.gdb" --batch </dev/null || :
%endif
  done

# Stop the port server
curl "http://localhost:${PORT_SERVER_PORT}/quitquitquit" || :
%endif

pushd src/python/grpcio_tests
for suite in \
    test_lite \
    %{?with_python_aio_tests:test_aio} \
    %{?with_python_gevent_tests:test_gevent} \
    test_py3_only
do
  echo "==== $(date -u --iso-8601=ns): Python ${suite} ===="
  # See the implementation of the %%pytest macro, upon which the following is
  # based. We add a timeout that is rather long, as it must apply to the entire
  # test suite. (Patching in a per-test timeout would be harder.)
  %{py3_test_envvars} timeout -k 31m -v 30m \
      %{python3} %{py_setup} %{?py_setup_args} "${suite}"
done
popd

%endif

%if %{without system_gtest}
# As a sanity check for our claim that gtest/gmock are not bundled, check
# installed executables for symbols that appear to have come from gtest/gmock.
foundgtest=0
if find %{buildroot} -type f -perm /0111 \
      -execdir objdump --syms --dynamic-syms --demangle '{}' '+' 2>/dev/null |
    grep -E '[^:]testing::'
then
  echo 'Found traces of gtest/gmock' 1>&2
  exit 1
fi
%endif


%files
%license LICENSE NOTICE.txt LICENSE-utf8_range
%{_libdir}/libaddress_sorting.so.%{c_so_version}{,.*}
%{_libdir}/libgpr.so.%{c_so_version}{,.*}
%{_libdir}/libgrpc.so.%{c_so_version}{,.*}
%{_libdir}/libgrpc_unsecure.so.%{c_so_version}{,.*}
%{_libdir}/libupb.so.%{c_so_version}{,.*}


%files data
%license LICENSE NOTICE.txt
%dir %{_datadir}/grpc/
%{_datadir}/grpc/roots.pem


%files doc
%license LICENSE NOTICE.txt

%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/CONCEPTS.md
%doc %{_pkgdocdir}/MAINTAINERS.md
%doc %{_pkgdocdir}/README.md
%doc %{_pkgdocdir}/SECURITY.md
%doc %{_pkgdocdir}/TROUBLESHOOTING.md

%doc %{_pkgdocdir}/doc/
%doc %{_pkgdocdir}/examples/



%files cpp
%{_libdir}/libgrpc++.so.%{cpp_so_version}{,.*}
%{_libdir}/libgrpc++_alts.so.%{cpp_so_version}{,.*}
%{_libdir}/libgrpc++_error_details.so.%{cpp_so_version}{,.*}
%{_libdir}/libgrpc++_reflection.so.%{cpp_so_version}{,.*}
%{_libdir}/libgrpc++_unsecure.so.%{cpp_so_version}{,.*}
%{_libdir}/libgrpc_plugin_support.so.%{cpp_so_version}{,.*}

%{_libdir}/libgrpcpp_channelz.so.%{cpp_so_version}{,.*}


%if %{with core_tests}
%files cli
%{_bindir}/grpc_cli
%{_libdir}/libgrpc++_test_config.so.%{cpp_so_version}
%{_mandir}/man1/grpc_cli.1*
%{_mandir}/man1/grpc_cli-*.1*
%endif


%files plugins
# These are for program use and do not offer a CLI for the end user, so they
# should really be in %%{_libexecdir}; however, too many downstream users
# expect them in $PATH to change this for the time being.
%{_bindir}/grpc_*_plugin


%files devel
%{_libdir}/libaddress_sorting.so
%{_libdir}/libgpr.so
%{_libdir}/libgrpc.so
%{_libdir}/libgrpc_unsecure.so
%{_libdir}/libupb.so
%{_includedir}/grpc/
%{_libdir}/pkgconfig/gpr.pc
%{_libdir}/pkgconfig/grpc.pc
%{_libdir}/pkgconfig/grpc_unsecure.pc
%{_libdir}/cmake/grpc/

%{_libdir}/libgrpc++.so
%{_libdir}/libgrpc++_alts.so
%{_libdir}/libgrpc++_error_details.so
%{_libdir}/libgrpc++_reflection.so
%{_libdir}/libgrpc++_unsecure.so
%{_libdir}/libgrpc_plugin_support.so
%{_includedir}/grpc++/
%{_libdir}/pkgconfig/grpc++.pc
%{_libdir}/pkgconfig/grpc++_unsecure.pc

%{_libdir}/libgrpcpp_channelz.so
%{_includedir}/grpcpp/


%files -n python3-grpcio
%license LICENSE NOTICE.txt LICENSE-utf8_range
%{python3_sitearch}/grpc/
%{python3_sitearch}/grpcio-%{pyversion}-py%{python3_version}.egg-info/


%files -n python3-grpcio-tools
%license LICENSE NOTICE.txt LICENSE-utf8_range
%{python3_sitearch}/grpc_tools/
%{python3_sitearch}/grpcio_tools-%{pyversion}-py%{python3_version}.egg-info/


%files -n python3-grpcio-channelz
%{python3_sitelib}/grpc_channelz/
%{python3_sitelib}/grpcio_channelz-%{pyversion}-py%{python3_version}.egg-info/


%files -n python3-grpcio-health-checking
%{python3_sitelib}/grpc_health/
%{python3_sitelib}/grpcio_health_checking-%{pyversion}-py%{python3_version}.egg-info/


%files -n python3-grpcio-reflection
%{python3_sitelib}/grpc_reflection/
%{python3_sitelib}/grpcio_reflection-%{pyversion}-py%{python3_version}.egg-info/


%files -n python3-grpcio-status
%{python3_sitelib}/grpc_status/
%{python3_sitelib}/grpcio_status-%{pyversion}-py%{python3_version}.egg-info/


%files -n python3-grpcio-testing
%{python3_sitelib}/grpc_testing/
%{python3_sitelib}/grpcio_testing-%{pyversion}-py%{python3_version}.egg-info/


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.48.4-55
- Latest state for grpc

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.48.4-54
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Sep 08 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-53
- Rebuilt for abseil-cpp 20250814.0

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.48.4-52
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.4-51
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 17 2025 Python Maint <python-maint@redhat.com> - 1.48.4-50
- Rebuilt for Python 3.14

* Mon May 26 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-49
- Rebuilt for abseil-cpp 20250512.0

* Fri May 02 2025 Kaleb S. KEITHLEY <kkeithle@redhat.com> - 1.48.4-48
- Remove openssl-devel-engine, and add associated patch

* Tue Feb 25 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-47
- Rebuilt for abseil-cpp-20250127.0

* Tue Feb 11 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-46
- Skip another ppc64le test

* Mon Feb 10 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-45
- Skip test_service_config, which times out
- This appears to be due to an unsafe combination of death tests and
  threads

* Wed Feb 05 2025 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-44
- Work around setuptools 74+ incompatiblity (close RHBZ#2319630)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.4-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 10 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.48.4-42
- Remove usage of coverage, per the packaging guidelines

* Sun Aug 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-41
- Rebuilt for abseil-cpp-20240722.0

* Wed Aug 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-40
- Rebuilt for re2-20240702

* Wed Aug 14 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-39
- Adjust to Changes/OpensslDeprecateEngine

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.4-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.48.4-37
- Rebuilt for Python 3.13

* Sun May 26 2024 U2FsdGVkX1 <U2FsdGVkX1@gmail.com> - 1.48.4-36
- Add riscv64 support

* Sat Feb 24 2024 Paul Wouters <paul.wouters@aiven.io> - 1.48.4-35
- Rebuilt for libre2.so.11 bump

* Sun Feb 04 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-34
- Rebuild for abseil-cpp-20240116.0

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.4-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-31
- Add missing includes for abseil-cpp-20240116.rc1

* Tue Nov 21 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.48.4-30
- Fix flatpak build

* Thu Nov 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-28
- Do not call PyEval_InitThreads (fix RHBZ#2247486)

* Wed Nov 01 2023 Miro Hrončok <miro@hroncok.cz> - 1.48.4-27
- Use Cython 3, specify noexcept for cdef functions

* Wed Oct 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-26
- F38+: Simplify Python test environment setup
- Use %%{py3_test_envvars}

* Tue Aug 29 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-25
- Rebuild for abseil-cpp-20230802.0

* Fri Jul 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-24
- Use the Cython compat package for now

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-22
- Use new (rpm 4.17.1+) bcond style

* Wed Jul 05 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-20
- Backport fix for CVE-2023-32732 (fix RHBZ#2214470)

* Thu Jun 22 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-19
- Improved find_module patch

* Thu Jun 22 2023 Python Maint <python-maint@redhat.com> - 1.48.4-18
- Rebuilt for Python 3.12

* Wed Jun 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-17
- Fix grpcio tests for Python 3.12

* Wed Jun 21 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-16
- Patch HTTP test server for Python 3.12

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.48.4-15
- Rebuilt for Python 3.12

* Fri May 12 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-14
- Add a trailing slash to one more directory in the files lists

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-13
- Add %%py_provides for importable modules

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-12
- List directories with trailing slashes

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-11
- List .so files more precisely

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-10
- Update rpmlintrc rules

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-9
- Hardlink duplicate files in the examples

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-8
- List doc/example files more explicitly
- Drop some less-relevant text documentation files

* Thu May 11 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-7
- Drop python3-grpcio-admin and python3-grpcio-csds subpackages

* Wed May 10 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.48.4-6
- Always disable xds-protos dependency in RHEL builds

* Tue Apr 25 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.48.4-5
- Revbump for ELN rebuild

* Sun Mar 05 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-4
- Post-bootstrap rebuild for abseil-cpp-20230125

* Sat Mar 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-3
- Bootstrap for abseil-cpp-20230125

* Sat Mar 04 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-2
- Skip a couple of new failing tests on aarch64 for abseil-cpp-20230125.0

* Thu Mar 02 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.4-1
- Update to 1.48.4

* Thu Feb 09 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.3-1
- Update to 1.48.3 (close RHBZ#2126980)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 10 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.2-2
- Update License to include header-only dependencies

* Sat Dec 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.2-1
- Update to 1.48.2

* Mon Nov 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.1-4
- More-correct .pc file path fix
- When passing paths to the build system, they are now correctly relative
  to the prefix rather than absolute.

* Wed Nov 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.1-3
- Fix wrong paths in .pc files

* Sat Sep 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.1-2
- Update test skips for 1.48.1

* Thu Sep 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.1-1
- Update to grpc 1.48.1 (close RHBZ#2123215)

* Fri Aug 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.0-2
- Update to grpc 1.48.0 (close RHBZ#2100262)

* Fri Aug 19 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.48.0-1
- Update to grpc 1.48.0 (bootstrap build)

* Sun Aug 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.47.1-1
- Update to 1.47.1

* Sat Aug 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-10
- Update License fields to SPDX

* Thu Aug 04 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-9
- Add dependency on grpc-plugins from grpc-devel

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.46.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 1.46.3-7
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.46.3-6
- Bootstrap for Python 3.11

* Fri Jun 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-5
- Work around ChannelzServicerTest Python 3.11 regressions for now
- Skips five failing tests. Closes RHBZ#2095027.

* Fri Jun 10 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-4
- Fix deprecated “inspect.getargspec”

* Fri May 27 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-3
- Use new upstream PR#25635 as .pc path fix

* Sat May 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-2
- Add exact-version dependency on grpc-cpp from grpc-cli

* Sat May 21 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.3-1
- Update to 1.46.3 (close RHBZ#2088859)

* Tue May 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.2-1
- Update to 1.46.2 (close RHBZ#2087019)

* Tue May 17 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.1-2
- Trivial typo fixes in spec file comments

* Sun May 15 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.46.1-1
- Update to 1.46.1 (close RHBZ#2024386)
- No longer depends on wyhash, as the core of the algorithm has been
  rewritten and included in the primary sources

* Mon May 02 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-21
- F37+: Stop tracking test failures on 32-bit arches

* Thu Mar 31 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-20
- Improve grpc-1.40.0-python-grpcio-use-system-abseil.patch

* Wed Mar 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-19
- Add exactly-versioned grpc-cpp subpackage dependencies

* Wed Mar 30 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-18
- Add virtual Provides for bundled upb to binary packages

* Mon Mar 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-17
- Skip client_ssl_test, which is prone to occasional timeouts

* Mon Mar 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-16
- Drop the NodeJS example’s package-lock.json file

* Wed Mar 09 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-15
- Rebuild for abseil-cpp 20211102.0 (non-bootstrap)

* Tue Mar 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-14
- Rebuild for abseil-cpp 20211102.0 (bootstrap)

* Tue Mar 08 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-13
- Rebuild for abseil-cpp 20211102.0

* Sat Feb 05 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-12
- Drop Conflicts with libgpr (fix RHBZ#2017576)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.41.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-10
- Add link to PR for GCC 12 fix

* Sun Jan 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-9
- Fix build on GCC 12

* Thu Jan 13 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-8
- Non-bootstrap rebuild

* Wed Jan 12 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-7
- Bootstrap after libre2.so.9 bump (fix RHBZ#2038546)

* Sat Jan 08 2022 Miro Hrončok <miro@hroncok.cz> - 1.41.1-6
- Rebuilt for libre2.so.9

* Tue Dec 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-5
- Dep. on cmake-filesystem is now auto-generated

* Fri Nov 05 2021 Adrian Reber <adrian@lisas.de> - 1.41.1-4
- Rebuilt for protobuf 3.19.0

* Tue Oct 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-3
- Add explicit Conflicts with libgpr for now (RHBZ#2017576)

* Tue Oct 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-2
- Fix mixed spaces and tabs in spec file

* Tue Oct 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.1-1
- Update to 1.41.1 (close RHBZ#20172232)

* Tue Oct 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.0-4
- Reduce macro indirection in the spec file

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 1.41.0-3
- Rebuilt for protobuf 3.18.1

* Tue Oct 12 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.0-2
- Update failing/skipped tests

* Wed Oct 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.41.0-1
- Update to 1.41.0

* Thu Sep 30 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.40.0-3
- Add missing python3-grpcio+protobuf extras metapackage

* Tue Sep 28 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.40.0-2
- Drop HTML documentation

* Fri Sep 17 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.40.0-1
- Update to 1.40.0 (close RHBZ#2002019)

* Wed Sep 15 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-10
- Trivial fix to grpc_cli-call man page

* Tue Sep 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-9
- Adapt to google-benchmark 1.6.0

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.39.1-8
- Rebuilt with OpenSSL 3.0.0

* Mon Aug 23 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-7
- Update some spec file comments

* Fri Aug 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-6
- Remove arguably-excessive use of the %%%%{name} macro

* Fri Aug 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-5
- No files need CRNL line ending fixes anymore

* Fri Aug 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-4
- Spiff up shebang-fixing snippet

* Fri Aug 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-3
- Remove executable permissions from more non-script sources, and send a PR
  upstream

* Fri Aug 20 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-2
- Some minor spec file cleanup

* Thu Aug 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.1-1
- Update to grpc 1.39.1 (close RHBZ#1993554)

* Thu Aug 19 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.0-3
- More updates to documented/skipped test failures

* Fri Aug 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.0-2
- Some updates to documented/skipped test failures

* Tue Aug 03 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.39.0-1
- Update to 1.39.0

* Wed Jul 21 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.37.1-10
- Simplify core test exclusion (no more useless use of cat)

* Fri Jul  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.37.1-8
- Use googletest 1.11.0

* Mon Jun 14 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.37.1-7
- Add BR on xxhash-static since we use it as a header-only library

* Thu Jun 10 2021 Rich Mattes <richmattes@gmail.com> - 1.37.1-6
- Rebuild for abseil-cpp-20210324.2

* Thu Jun 10 2021 Stephen Gallagher <sgallagh@redhat.com> - 1.37.1-5
- Fix builds against Python 3.10 on ELN/RHEL as well

* Thu Jun 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.37.1-4
- Since it turns out xxhash is used as a header-only library, we can stop
  patching the source to unbundle it; removing the bundled copy suffices

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.37.1-3
- Rebuilt for Python 3.10

* Fri May 21 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.37.1-2
- Use full gRPC_{CPP,CSHARP}_SOVERSION in file globs

* Tue May 11 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.37.1-1
- General:
  * New version 1.37.1
  * Drop patches that were upstreamed since the last packaged release, were
    backported from upstream in the first place, or have otherwise been
    obsoleted by upstream changes.
  * Rebase/update remaining patches as needed
  * Drop Fedora 32 compatibility
  * Add man pages for grpc_cli
- C (core) and C++ (cpp):
  * Switch to CMake build system
  * Build with C++17 for compatibility with the abseil-cpp package in Fedora
  * Add various Requires to -devel subpackage

* Tue Apr 06 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.0-15
- General:
  * Do not use %%exclude for unpackaged files (RPM 4.17 compatibility)
- Python:
  * Stop using %%pyproject_buildrequires, since it is difficult to fit the
    pyproject-rpm-macros build and install macros into this package, and Miro
    Hrončok has advised that “mixing %%pyproject_buildrequires with
    %%py3_build/%%py3_install is generally not a supported way of building
    Python packages.”

* Thu Mar 25 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.0-14
- General:
  * Improved googletest source URL (better tarball name)

* Tue Mar 23 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.0-13
- General:
  * Replace * with • in descriptions
  * Use cmake() dependencies first, and pkgconfig() dependencies second, where
    available
  * Drop explicit pkgconfig BR
  * Fix the directory in which CMake installs pkgconfig files
  * Improved CMake options
  * Build the Doxygen reference manuals
- C (core) and C++ (cpp):
  * Let the -devel package require cmake-filesystem
  * Allow building tests with our own copy of gtest/gmock, which will become
    mandatory when we depend on abseil-cpp and switch to C++17
  * Fix a link error in the core tests when using CMake
  * Manually install grpc_cli (CMake)
  * Add CMake files to the files list for the -devel package
  * Start running some of the core tests in %%check
- Python:
  * Add several patches required for the tests
  * BR gevent for gevent_tests
  * Fix build; in particular, add missing preprocess and build_package_protos
    steps, without which the packages were missing generated proto modules and
    were not
    usable!
  * Add %%py_provides for Fedora 32
  * Drop python3dist(setuptools) BR, redundant with %%pyproject_buildrequires
  * Start running most of the Python tests in %%check
  * Merge the python-grpcio-doc subpackage into grpc-doc

* Tue Feb 16 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.0-12
- C (core) and C++ (cpp):
  * Add CMake build support but do not enable it yet; there is still a problem
    where grpc_cli is only built with the tests, and a linking problem when
    building the tests

* Tue Feb 02 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.26.0-11
- General:
  * Update summaries and descriptions
  * Update License fields to include licenses from bundled components
  * Fix failure to respect Fedora build flags
  * Use the system shared certificate bundle instead of shipping our own
- CLI:
  * No longer set rpath $ORIGIN
- C (core) and C++ (cpp):
  * Add c_so_version/cpp_so_version macros
  * Split out C++ bindings and shared data into subpackages
  * Drop obsolete ldconfig_scriptlets macro
  * Stop stripping debugging symbols
- Python:
  * Use generated BR’s
  * Build and package Python binding documentation
  * Disable accommodations for older libc’s
  * Patch out -std=gnu99 flag, which is inappropriate for C++
  * Build additional Python packages grpcio_tools, gprcio_channelz,
    grpcio_health_checking, grpcio_reflection, grpcio_status, and
    grpcio_testing

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 08:46:34 CET 2021 Adrian Reber <adrian@lisas.de> - 1.26.0-9
- Rebuilt for protobuf 3.14

* Fri Nov 13 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 1.26.0-8
- build: disable LTO due to rh#1893533

* Thu Sep 24 2020 Adrian Reber <adrian@lisas.de> - 1.26.0-7
- Rebuilt for protobuf 3.13

* Mon Aug 03 2020 Gwyn Ciesla <gwync@protonmail.com> - 1.26.0-6
- Patches for https://github.com/grpc/grpc/pull/21669

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de> - 1.26.0-4
- Rebuilt for protobuf 3.12

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.26.0-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.26.0-1
- Update to 1.26.0

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 1.20.1-5
- Rebuild for protobuf 3.11

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.20.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.20.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.20.1-1
- Update to 1.20.1

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.18.0-1
- Update to 1.18.0

* Mon Dec 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.17.1-3
- Properly store patch in SRPM

* Mon Dec 17 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.1-2
- Build without ruby plugin for Fedora < 30 (Thanks to Mathieu Bridon)

* Fri Dec 14 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.1-1
- Update to 1.17.1 and package python bindings

* Fri Dec 07 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 1.17.0-1
- Initial revision

## END: Generated by rpmautospec
