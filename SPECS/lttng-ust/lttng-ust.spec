Summary:        LTTng-UST is an Userspace Tracer library
Name:           lttng-ust
Version:        2.13.6
Release:        1%{?dist}
License:        GPLv2+ and LGPLv2+ and MIT
URL:            https://lttng.org
Source0:        https://lttng.org/files/%{name}/%{name}-%{version}.tar.bz2
Group:          Development/Libraries
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires: libnuma-devel
BuildRequires: userspace-rcu-devel
%if %{with_check}
BuildRequires: perl
%endif

Requires:      userspace-rcu

%description
This library may be used by user-space applications to generate
trace-points using LTTng.

%package devel
Summary:       The libraries and header files needed for LTTng-UST development.
Requires:      %{name} = %{version}-%{release}

%description devel
The libraries and header files needed for LTTng-UST development.

%prep
%setup -q

%build
./configure \
   --prefix=%{_prefix} \
   --docdir=%{_docdir}/%{name} \
   --disable-static

make %{?_smp_mflags}

%check
make %{?_smp_mflags} check

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/lttng-ust*.pc

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.6-1
- Auto-upgrade to 2.13.6 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.13.1-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

*   Fri Jan 14 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.13.1-1
-   Upgrading to 2.13.1

*   Thu May 21 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.11.2-1
-   Updating to version 2.11.2.
-   Updating the "Source0" and "URL" tags.
-   Removing the "sha1" macro.
-   License verified.

*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.10.2-4
-   Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.10.2-3
-   Initial CBL-Mariner import from Photon (license: Apache2).

*   Wed Jan 02 2019 Keerthana K <keerthanak@vmware.com> 2.10.2-2
-   Added make check.

*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.10.2-1
-   Update to version 2.10.2

*   Mon Dec 19 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.9.0-1
-   Initial build.  First version
