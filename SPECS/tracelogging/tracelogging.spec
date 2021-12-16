Summary:        tracelogging one-line structure logging API on top of LTTNG
Name:           tracelogging
Version:        0.2
Release:        3%{?dist}
License:        MIT
URL:            https://github.com/microsoft/tracelogging
Group:          System Environment
Vendor:         Microsoft Corporation
Distribution:   Mariner

#Source0:       https://github.com/microsoft/%{name}/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  catch-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  lttng-ust-devel

%if %{with_check}
BuildRequires:  catch-devel
%endif

%description
The tracelogging for LTTNG project enables structured event emission through
LTTNG via the same set of macros that are supported by the publicly
available tracelogging for ETW project in the Windows SDK.

%package        devel
Summary:        Development files for tracelogging
License:        MIT
Group:          System Environment/Libraries
Requires:       tracelogging = %{version}-%{release}

%description    devel
This package contains the headers and symlinks for instrumenting
applications and libraries with tracelogging.

%prep
%setup

%build
mkdir build && cd build
%cmake ..
%make_build

%check
make test -C build

%install
%make_install -C build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
*   Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2-3
-   Removing the explicit %%clean stage.

*   Wed Oct 14 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 0.2-2
-   Added source URL.
-   License verified.
*   Tue Feb 11 2020 Nick Bopp <nichbop@microsoft.com> 0.2-1
-   Original version for CBL-Mariner.