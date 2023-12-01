Summary:        tracelogging one-line structure logging API on top of LTTNG
Name:           tracelogging
Version:        0.3.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment
URL:            https://github.com/microsoft/tracelogging
Source0:        https://github.com/microsoft/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake >= 3.6
BuildRequires:  gcc
BuildRequires:  lttng-ust-devel >= 2.13
%if %{with_check}
BuildRequires:  catch-devel > 2.0
%endif

%description
The tracelogging for LTTNG project enables structured event emission through
LTTNG via the same set of macros that are supported by the publicly
available tracelogging for ETW project in the Windows SDK.

%package        devel
Summary:        Development files for tracelogging
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains the headers and symlinks for instrumenting
applications and libraries with tracelogging.

%prep
%autosetup

%build
mkdir build && cd build
%cmake \
%if %{with_check}
    -DTRACELOGGING_BUILD_TESTS=ON \
%else
    -DTRACELOGGING_BUILD_TESTS=OFF \
%endif
    ..
%make_build

%check
%make_build test -C build

%install
%make_install -C build

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%doc README.md
%license LICENSE
%{_libdir}/liblttngh.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/lttngh
%{_includedir}/tracelogging
%{_libdir}/liblttngh.so
%{_libdir}/cmake/tracelogging

%changelog
* Wed Feb 09 2022 Francisco Huelsz Prince <frhuelsz@microsoft.com> - 0.3.1-1
- Upgrade to 0.3.1 for lttng-ust 2.13 compatibility & fixes.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.3-1
- Upgrade to latest upstream version for lttng-ust 2.13 compatibility
- Use CMake options to avoid pulling in catch-devel in non-test builds
- Add version constraints to requirements
- Lint spec

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2-3
- Removing the explicit %%clean stage.

* Wed Oct 14 2020 Pawel Winogrodzki <pawelwi@microsoft.com> = 0.2-2
- Added source URL.
- License verified.

* Tue Feb 11 2020 Nick Bopp <nichbop@microsoft.com> 0.2-1
- Original version for CBL-Mariner.
