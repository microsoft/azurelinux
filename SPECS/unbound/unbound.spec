Summary:        unbound dns server
Name:           unbound
Version:        1.17.1
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Servers
URL:            https://nlnetlabs.nl/projects/unbound/about/
Source0:        https://github.com/NLnetLabs/%{name}/archive/release-%{version}.tar.gz#/%{name}-release-%{version}.tar.gz
Source1:        %{name}.service
BuildRequires:  expat-devel
BuildRequires:  libevent-devel
BuildRequires:  python3-devel
BuildRequires:  swig
BuildRequires:  systemd
Requires:       systemd
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Provides:       %{name}-libs = %{version}-%{release}

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package        devel
Summary:        unbound development libs and headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       expat-devel

%description    devel
Development files for unbound dns server

%package -n     python3-%{name}
Summary:        Python 3 bindings for %{name}
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for %{name}

%package        docs
Summary:        unbound docs
Group:          Documentation

%description docs
unbound dns server docs

%prep
%autosetup -p1 -n %{name}-release-%{version}

%build
%configure \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static \
    --with-pythonmodule \
    --with-pyunbound \
    --with-libevent \
    PYTHON=%{python3}
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
make DESTDIR=%{buildroot} unbound-event-install
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
%make_build check

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/*.so.*
%{_sbindir}/*
%{_sysconfdir}/*
%{_unitdir}/%{name}.service

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%files -n python3-%{name}
%{python3_sitelib}/*

%files docs
%{_mandir}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.17.1-1
- Auto-upgrade to 1.17.1 - Azure Linux 3.0 - package upgrades

* Wed Oct 12 2022 Henry Li <lihl@microsoft.com> - 1.16.3-1
- Upgrade to version 1.16.3 to resolve CVE-2022-3204

* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 1.16.2-1
- Bump version to address CVE-2022-30698

* Fri Jul 08 2022 Rachel Menge <rachelmenge@microsoft.com> - 1.13.2-2
- Build with libevent

* Fri Jan 14 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.13.2-1
- Update to version 1.13.2.

* Fri Jul 23 2021 Thomas Crain <thcrain@microsoft.com> - 1.10.0-5
- Add provides for libs subpackage from base package
- Add python3 modules subpackage

*  Mon Dec 21 2020 Rachel Menge <rachelmenge@microsoft.com> - 1.10.0-4
-  Fix CVE-2020-28935.

*  Tue Oct 20 2020 Joe Schmitt <joschmit@microsoft.com> 1.10.0-3
-  Fix CVE-2020-12662 and CVE-2020-12663.

*  Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.10.0-2
-  Added %%license line automatically

*  Fri May 01 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.10.0-1
-  Bumping version up to 1.10.0 to fix CVE-2019-16866 and CVE-2019-18934.
-  Fixed "Source0" and "URL" tags.
-  License verified.

*  Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.8.0-2
-  Initial CBL-Mariner import from Photon (license: Apache2).

*  Mon Sep 10 2018 Michelle Wang <michellew@vmware.com> 1.8.0-1
-  Update to version 1.8.0.

*  Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-3
-  Remove shadow from requires and use explicit tools for post actions

*  Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 1.6.1-2
-  Requires expat-devel

*  Wed Apr 05 2017 Xiaolin Li <xiaolinl@vmware.com> 1.6.1-1
-  Updated to version 1.6.1

*  Fri Jan 06 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.6.0-1
-  Initial
