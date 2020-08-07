Summary:        LTTng is an open source tracing framework for Linux.
Name:           lttng-tools
Version:        2.11.2
Release:        1%{?dist}
License:        GPLv2 and LGPLv2+
URL:            https://lttng.org/
Source0:        https://lttng.org/files/lttng-tools/%{name}-%{version}.tar.bz2
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires: libxml2-devel >= 2.7.6
BuildRequires: nss-devel
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel
BuildRequires: userspace-rcu-devel >= 0.8.0
BuildRequires: lttng-ust-devel >= 2.9.0
Requires:      lttng-ust = %{version}
Requires:      userspace-rcu
Requires:      elfutils
Requires:      nss
Requires:      libxml2

%description
LTTng is an open source tracing framework for Linux.

%prep
%setup -q

%build
%configure \
   --prefix=%{_prefix}

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name '*.la' -delete

%files
%license LICENSE
%{_bindir}/*
%{_includedir}/*
%{_lib}/*
%{_datadir}/*
%exclude %{_libdir}/debug

%changelog
*   Thu May 21 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.11.2-1
-   Updating to version 2.11.2.
-   Adding explicit dependency on "lttng-ust".
-   Removing invalid "--disable-lttng-ust" flag.
-   Fixing the "Vendor" tag.
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 2.10.5-4
-   Added %%license line automatically
*   Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 2.10.5-3
-   Fix Source0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.10.5-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 2.10.5-1
-   Update to version 2.10.5
*   Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 2.9.4-1
-   Update package version
*   Tue Jul 26 2016 Divya Thaluru <dthaluru@vmware.com> 2.7.1-3
-   Added userspace-rcu-devel as build time dependent package
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.1-2
-   GA - Bump release of all rpms
*   Thu Jan 28 2016 Xiaolin Li <xiaolinl@vmware.com> 2.7.1-1
-   Updated to version 2.7.1
*   Tue Nov 24 2015 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-1
-   Initial build.  First version
