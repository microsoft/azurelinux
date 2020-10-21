Summary:        unbound dns server
Name:           unbound
Version:        1.10.0
Release:        3%{?dist}
Group:          System/Servers
Vendor:         Microsoft Corporation
License:        BSD
Distribution:   Mariner
URL:            https://nlnetlabs.nl/projects/unbound/about/
#Source0:       https://github.com/NLnetLabs/%{name}/archive/release-%{version}.tar.gz
Source0:        %{name}-release-%{version}.tar.gz
Source1:        %{name}.service

# CVE-2020-12662.patch also fixes CVE-2020-12663
Patch0:         CVE-2020-12662.patch
Patch1:         CVE-2020-12663.nopatch

BuildRequires:  systemd
BuildRequires:  expat-devel

Requires:       systemd
Requires(pre):  /usr/sbin/useradd /usr/sbin/groupadd

%description
Unbound is a validating, recursive, and caching DNS resolver.

%package    devel
Summary:    unbound development libs and headers
Group:      Development/Libraries
Requires:   expat-devel

%description devel
Development files for unbound dns server

%package    docs
Summary:    unbound docs
Group:      Documentation

%description docs
unbound dns server docs

%prep
%setup -q -n %{name}-release-%{version}
%patch0 -p1

%build
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --with-conf-file=%{_sysconfdir}/%{name}/unbound.conf \
    --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
find %{buildroot} -name '*.la' -delete
install -vdm755 %{buildroot}%{_unitdir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%check
make check

%pre
getent group unbound >/dev/null || groupadd -r unbound
getent passwd unbound >/dev/null || \
useradd -r -g unbound -d %{_sysconfdir}/unbound -s /sbin/nologin \
-c "Unbound DNS resolver" unbound

%post
    /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

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

%files docs
%{_mandir}/*

%changelog
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
