## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 9;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


# LTO (more specifically -ffat-lto-objects) breaks compilation
# due to inconsistent decls in the header macros
# CPPMICROSERVICES_IMPORT_BUNDLE & CPPMICROSERVICES_INITIALIZE_BUNDLE
# and trying the obvious fix caused a ripple effect breaking other
# areas
%global _lto_cflags %nil

#  usFrameworkTests fail with "Resource temporarily unavailable"
%ifarch %{ix86}
%global with_tests 0
%else
%global with_tests 1
%endif

Name: CppMicroServices
Version: 3.8.5
Release: %autorelease
Summary: C++ components for building service-oriented applications
Url: http://cppmicroservices.org/

License: %{shrink:
  Apache-2.0 AND
  %dnl third_party/tinyscheme
  BSD-3-Clause AND
  %dnl framework/include/cppmicroservices/Any.h
  %dnl webconsole/include/cppmicroservices/webconsole/mustache.hpp
  BSL-1.0 AND
  %dnl webconsole/resources/res/*.{jss,css}
  %dnl third_party/{rapidjson,optionparser,miniz}
  MIT
}

Source0: https://github.com/CppMicroServices/CppMicroServices/archive/refs/tags/v%{version}.tar.gz#/CppMicroServices-%{version}.tar.gz

# Raised issue upstream to discuss possibility of officially
# supporting more system libraries to eliminate carrying these
# patches:
#
#   https://github.com/CppMicroServices/CppMicroServices/issues/1060
#
# Patches maintained in:
#
#  https://github.com/berrange/CppMicroServices/commits/fedora-dist/
#
Patch: 0001-Fully-use-system-boost.patch
Patch: 0002-Use-system-jsoncpp-library.patch
Patch: 0003-Use-system-linenoise-library.patch
Patch: 0004-Use-system-civetweb-package.patch
Patch: 0005-Use-system-spdlog-package.patch
Patch: 0006-Removed-unused-absl-package.patch
Patch: 0007-Replace-use-of-removed-htmlescape-function-from-sphi.patch
Patch: 0008-Remove-broken-docs-python-monkeypatching.patch
# https://github.com/CppMicroServices/CppMicroServices/pull/1057
Patch: 0009-framework-include-cppmicroservces-add-missing-cstdin.patch
Patch: 0010-Fix-for-system-libraries-for-gmock-google-benchmark.patch
Patch: 0011-Use-fPIC-on-all-architectures-not-just-x86_64.patch
Patch: 0012-Disable-JSON-comment-test.patch

# Regardless of the above issue wrt system libraries, the following
# are likely to need carrying as bundled libraries indefinitely in
# Fedora. See later comments in this spec where we remove all of
# the 'third_party/' directory contents except for these four.
#
# Needs git snapshot which is not available in Fedora
Provides: bundled(rapidjson) = 091de040edb3355dcf2f4a18c425aec51b906f08
# Non-upstream modifications
Provides: bundled(miniz) = 3.0.2
# Non-upstream modifications
Provides: bundled(optionparser) = 1.7
# Not available in Fedora
Provides: bundled(tinyscheme) = 1.41

BuildRequires: gcc-c++
BuildRequires: doxygen
BuildRequires: cmake
BuildRequires: boost-devel
BuildRequires: civetweb-devel
BuildRequires: jsoncpp-devel
BuildRequires: linenoise-devel
BuildRequires: rapidjson-devel
BuildRequires: spdlog-devel
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme
BuildRequires: python3-breathe
%if %{with_tests}
BuildRequires: gmock-devel
BuildRequires: google-benchmark-devel
BuildRequires: gtest-devel
BuildRequires: lsof
%endif

%description
The C++ Micro Services project is a collection of components for
building modular and dynamic service-oriented applications. It
is based on OSGi, but tailored to support native cross-platform
solutions.

%package devel
Summary: Development files for CppMicroServices
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The C++ Micro Services project is a collection of components for
building modular and dynamic service-oriented applications. It
is based on OSGi, but tailored to support native cross-platform
solutions.

This provides the development headers and libraries.

%package docs
Summary: Development files for CppMicroServices
Requires: %{name}%{?_isa} = %{version}-%{release}

%description docs
The C++ Micro Services project is a collection of components for
building modular and dynamic service-oriented applications. It
is based on OSGi, but tailored to support native cross-platform
solutions.

This provides the library documentation

%prep
%autosetup -p1

# No longer used by code:
#   https://github.com/CppMicroServices/CppMicroServices/pull/1058
rm -rf third_party/absl

# Patched to use Fedora package
rm -rf third_party/benchmark

# Patched to use Fedora package
rm -rf third_party/boost

# Patched to use Fedora package
rm -rf third_party/civetweb

# Not really third party code AFAICT, so not
# applicable to unbundle
#rm -rf third_party/cppmicroservices_pe.h

# Not applicable to Linux build
rm -rf third_party/dirent_win32.h

# Patched to use Fedora package
rm -rf third_party/googletest

# Patched to use Fedora package
rm -rf third_party/json
rm -rf third_party/jsoncpp.cpp

# Never actually used by the code:
#   https://github.com/CppMicroServices/CppMicroServices/pull/1059
rm -rf third_party/libtelnet*

# Patched to use Fedora package
rm -rf third_party/linenoise*

# Has local modifications adding features that are not
# in upstream so can't use standard Fedora package
#rm -rf third_party/miniz*

# Not in Fedora and has local modifications adding
# features that are not in upstream so undesirable
# to add a Fedora package
#rm -rf third_party/optionparser.h

# Needs git master. Upstream is dead and won't be making
# any more releases:
#
#    https://github.com/Tencent/rapidjson/issues/1006
#
# Fedora has 1.1.0 and is resisting shipping git snapshots:
#
#    https://lists.fedorahosted.org/archives/list/devel@lists.fedoraproject.org/message/RKNCGOALWVIEYMIB5ZRPTVSH5EDG4NGU/
#rm -rf third_party/rapidjson

# Patched to use Fedora package
rm -rf third_party/spdlog

# Not in Fedora, and has build time settings for controlling
# available features that are intended to be set to match
# the application's required usage.
#rm -rf third_party/tinyscheme

%build
# We set 'memcheck' command to /bin/true as running
# tests under memcheck takes 1hr20 even on a fast
# x86_64 machine. This is unreasonably long for
# unit tests considering some architectures are
# far slower
%cmake \
  -DUS_USE_SYSTEM_BOOST:BOOL=ON \
%if %{with_tests}
  -DUS_USE_SYSTEM_GTEST:BOOL=ON \
  -DUS_BUILD_TESTING:BOOL=ON \
  -DUS_MEMCHECK_COMMAND:PATH=/bin/true \
%else
  -DUS_BUILD_TESTING:BOOL=OFF \
%endif
  -DUS_BUILD_DOC_HTML:BOOL=ON \
  -DUS_BUILD_DOC_MAN:BOOL=ON \
  -DLIBRARY_INSTALL_DIR=%{_libdir} \
  -DTOOLS_INSTALL_DIR=%{_bindir} \
  -DRUNTIME_INSTALL_DIR=%{_bindir} \
  -DARCHIVE_INSTALL_DIR=%{_libdir} \
  -DHEADER_INSTALL_DIR=%{_includedir}/cppmicroservices3 \
  -DAUXILIARY_INSTALL_DIR=%{_datadir}/cppmicroservices3 \
  -DDOC_INSTALL_DIR=%{_datadir}/doc/cppmicroservices3 \
  -DMAN_INSTALL_DIR=%{_mandir}
%cmake_build

%install
%cmake_install

%check
%if %{with_tests}
%cmake_build -t test || (
  echo "==================== TEST LOGS ===================="
  cat %{__cmake_builddir}/Testing/Temporary/LastTest.log;
  exit 1
)
%endif

%files
%license LICENSE
%{_libdir}/libConfigurationAdmind.so.*
%{_libdir}/libCppMicroServicesd.so.*
%{_libdir}/libDeclarativeServicesd.so.*
%{_libdir}/libLogServiced.so.*
# NB: not a versioned library :-(
%{_libdir}/libusAsyncWorkServiced.so
# NB: not a versioned library :-(
%{_libdir}/libusEMd.so
%{_libdir}/libusHttpServiced.so.*
# NB: not a versioned library :-(
%{_libdir}/libusServiceComponentd.so
%{_libdir}/libusShellServiced.so.*
%{_libdir}/libusWebConsoled.so.*

%files devel
%{_datadir}/cppmicroservices3
%{_includedir}/cppmicroservices3
%{_bindir}/SCRCodeGen3
%{_bindir}/jsonschemavalidator
%{_bindir}/usResourceCompiler3
%{_bindir}/usShell3
%{_libdir}/libConfigurationAdmind.so
%{_libdir}/libCppMicroServicesd.so
%{_libdir}/libDeclarativeServicesd.so
%{_libdir}/libLogServiced.so
%{_libdir}/libusHttpServiced.so
%{_libdir}/libusShellServiced.so
%{_libdir}/libusWebConsoled.so
%{_mandir}/man1/usResourceCompiler3.1*
%{_mandir}/man1/usShell3.1*
%{_mandir}/man3/cppmicroservices-asyncworkservice.3*
%{_mandir}/man3/cppmicroservices-configadmin.3*
%{_mandir}/man3/cppmicroservices-ds.3*
%{_mandir}/man3/cppmicroservices-framework.3*
%{_mandir}/man3/cppmicroservices-httpservice.3*
%{_mandir}/man3/cppmicroservices-logservice.3*
%{_mandir}/man3/cppmicroservices-shellservice.3*
%{_mandir}/man3/cppmicroservices-webconsole.3*
%{_mandir}/man3/cppmicroservices.3*
%{_mandir}/man7/cppmicroservices-httpservice.7*
%{_mandir}/man7/cppmicroservices-shellservice.7*
%{_mandir}/man7/cppmicroservices-webconsole.7*
%{_mandir}/man7/cppmicroservices.7*

%files docs
%{_datadir}/doc/cppmicroservices3

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.8.5-9
- Latest state for CppMicroServices

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar 07 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-7
- Disable comment test that's broken with new jsoncpp

* Fri Mar 07 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-6
- Rebuild for libjsoncpp soname break

* Wed Feb 05 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-5
- Properly disable tests on i686

* Wed Feb 05 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-4
- Add missing patch from previous commit

* Wed Feb 05 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-3
- Disable tests on i686 since they fail

* Wed Feb 05 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-2
- Add lsof needed by tests and dump test logs on failure

* Wed Feb 05 2025 Daniel P. Berrangé <berrange@redhat.com> - 3.8.5-1
- Initial import
## END: Generated by rpmautospec
