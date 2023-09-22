Summary:        LTTng is an open source tracing framework for Linux.
Name:           lttng-tools
Version:        2.13.2
Release:        2%{?dist}
License:        GPLv2 and LGPLv2+
URL:            https://lttng.org/
Source0:        https://lttng.org/files/%{name}/%{name}-%{version}.tar.bz2
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires: libxml2-devel >= 2.7.6
BuildRequires: m4
BuildRequires: elfutils-devel
BuildRequires: popt-devel
BuildRequires: userspace-rcu-devel >= 0.8.0
BuildRequires: lttng-ust-devel >= 2.13.1
Requires:      lttng-ust >= 2.13.1
Requires:      userspace-rcu >= 0.8.0
Requires:      elfutils
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
%{_libdir}/*
%{_datadir}/*
%exclude %{_libdir}/debug

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.13.2-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Fri Jan 14 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 2.13.2-1
- Upgrading to 2.13.2
- Updated source url.
- Updating lttng-ust requirement to version 2.13.1.
- Removing unnecessary nss requirement.
- Updating userspace-rcu requirement version.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.11.2-2
- Replace incorrect %%{_lib} usage with %%{_libdir}

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
