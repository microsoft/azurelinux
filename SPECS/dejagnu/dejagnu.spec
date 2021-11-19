Summary:        DejaGnu test framework
Name:           dejagnu
Version:        1.6.3
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://www.gnu.org/software/dejagnu
Source0:        https://ftp.gnu.org/pub/gnu/dejagnu/%{name}-%{version}.tar.gz
BuildRequires:  expect-devel
Requires:       expect
Requires(post): texinfo
Requires(postun): texinfo
BuildArch:      noarch

%description
DejaGnu is a framework for testing other programs. Its purpose is to provide
a single front end for all tests. Think of it as a custom library of Tcl
procedures crafted to support writing a test harness. A test harness is the
testing infrastructure that is created to support a specific program or tool.
Each program can have multiple testsuites, all supported by a single test
harness. DejaGnu is written in Expect, which in turn uses Tcl.

%package devel
Summary:        Headers and development libraries for dejagnu
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       expect-devel

%description devel
Headers and development libraries for dejagnu

%prep
%setup -q

%build
./configure \
    --prefix=%{_prefix}
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

%post
%{_bindir}/install-info --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%postun
%{_bindir}/install-info --delete --info-dir=%{_infodir} %{_infodir}/%{name}.info.gz

%files
%defattr(-,root,root)
%license COPYING
%{_bindir}/*
%{_datadir}/dejagnu/*
%{_infodir}/*
%exclude %{_infodir}/dir
%{_mandir}/*

%files devel
%defattr(-,root,root)
%{_includedir}/*

%changelog
* Wed Nov 10 2021 Chris Co <chrco@microsoft.com> - 1.6.3-1
- Update to 1.6.3
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.6.2-2
- Added %%license line automatically

* Mon Apr 13 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.6.2-1
- Update to 1.6.2.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.6-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Ajay Kaher <akaher@vmware.com> - 1.6-1
- Upgraded to version 1.6

* Thu Jul 13 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.5.3-1
- Initial build. First version
