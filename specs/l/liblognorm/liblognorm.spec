# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define htmldir %{_docdir}/liblognorm/html

Name:		liblognorm
Version:	2.0.6
Release: 17%{?dist}
Summary:	Fast samples-based log normalization library
License:	LGPL-2.1-or-later AND Apache-2.0
URL:		http://www.liblognorm.com
Source0:	http://www.liblognorm.com/files/download/%{name}-%{version}.tar.gz

BuildRequires:	gcc
BuildRequires:	chrpath
BuildRequires:	libfastjson-devel
BuildRequires:	libestr-devel
BuildRequires:	pcre2-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool

Patch0: liblognorm-2.0.6-rhbz2105934-sphinx5.patch
Patch1: liblognorm-configure-glitch.patch
Patch2: liblognorm-2.0.6-rhbz2128320.patch

%description
Briefly described, liblognorm is a tool to normalize log data.

People who need to take a look at logs often have a common problem. Logs from
different machines (from different vendors) usually have different formats for
their logs. Even if it is the same type of log (e.g. from firewalls), the log
entries are so different, that it is pretty hard to read these. This is where
liblognorm comes into the game. With this tool you can normalize all your logs.
All you need is liblognorm and its dependencies and a sample database that fits
the logs you want to normalize.

%package devel
Summary:	Development tools for programs using liblognorm library
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	json-c-devel%{?_isa}
Requires:	libestr-devel%{?_isa}

%description devel
The liblognorm-devel package includes header files, libraries necessary for
developing programs which use liblognorm library.

%package doc
Summary: HTML documentation for liblognorm
BuildRequires: python3-sphinx
BuildRequires: make

%description doc
This sub-package contains documentation for liblognorm in a HTML form.

%package utils
Summary:	Lognormalizer utility for normalizing log files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description utils
The lognormalizer is the core of liblognorm, it is a utility for normalizing
log files.

%prep
%setup -q

%patch -P 0 -p1 -b .sphinx5
%patch -P 1 -p1 -b .configure-glitch
%patch -P 2 -p1 -b .pcre2

%build
# Prevent rebuild of the configure script.
touch configure aclocal.m4 Makefile.in config.h.in
autoreconf --verbose --force --install
%configure --enable-regexp --enable-docs --docdir=%{htmldir} --includedir=%{_includedir}/%{name}/


%install
make V=1 install INSTALL="install -p" DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.{a,la}
chrpath -d %{buildroot}%{_bindir}/lognormalizer
chrpath -d %{buildroot}%{_libdir}/liblognorm.so
rm %{buildroot}%{htmldir}/{objects.inv,.buildinfo}

%ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc AUTHORS ChangeLog README
%exclude %{htmldir}

%{_libdir}/lib*.so.*

%files devel
%{_libdir}/lib*.so
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/*.pc

%files doc
%doc %{htmldir}

%files utils
%{_bindir}/lognormalizer


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Attila Lakatos <alakatos@redhat.com> - 2.0.6-9
- Port pcre dependency to pcre2
  resolves: rhbz#2128320

* Wed May 31 2023 Attila Lakatos <alakatos@redhat.com> - 2.0.6-8
- Update License tag for SPDX
- Apache 2.0 was missing according to upstream sources

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Florian Weimer <fweimer@redhat.com> - 2.0.6-6
- Fix configure.ac/configure glitch (#2141801)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Attila Lakatos <alakatos@redhat.com> - 2.0.6-4
- Update language to comply with sphinx5
  resolves: rhbz#2105934

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Attila Lakatos <alakatos@redhat.com> - 2.0.6-1
- Rebase to 2.0.6

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 12 2017 Marek Tamaskovic <mtamasko@redhat.com> - 2.0.3-4
- Fix header files location
- resolves rhbz#1113573

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Radovan Sroka <rsroka@redhat.com> - 2.0.2-1
- rebase to 2.0.3

* Thu Feb 9 2017 Radovan Sroka <rsroka@redhat.com> - 2.0.2-2
- removed forgoten commented line

* Thu Feb 9 2017 Radovan Sroka <rsroka@redhat.com> - 2.0.2-1
- rebase to 2.0.2

* Tue Oct 4 2016 Radovan Sroka <rsroka@redhat.com> - 2.0.1-1
- rebase to 2.0.1

* Tue Mar 15 2016 Radovan Sroka <rsroka@redhat.com> - 1.1.3-1
- rebase to v1.1.3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar 15 2015 Tomas Heinrich <theinric@redhat.com> - 1.1.1-1
- rebase to 1.1.1 (soname bump)
  - drop liblognorm-0.3.4-pc-file.patch, not needed anymore
  - update dependencies for the new version
  - add a new subpackage for documentation
  - enable support for reqular expressions
- make build more verbose

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jul 31 2013 Tomas Heinrich <theinric@redhat.com> - 0.3.7-1
- rebase to 0.3.7

* Wed Dec 12 2012 Mahaveer Darade <mah.darade@gmail.com> - 0.3.5-1
- upgrade to upstream version 0.3.5
- drop patch0, merged upstream
  liblognorm-0.3.4-rename-to-lognormalizer.patch
- remove trailing whitespace

* Fri Oct 05 2012 mdarade <mdarade@redhat.com> - 0.3.4-4
- Modified description of main & util package

* Thu Sep 20 2012 Mahaveer Darade <mdarade@redhat.com> - 0.3.4-3
- Renamed normalizer binary to lognormalizer
- Updated pc file to exclude lee and lestr

* Mon Aug 27 2012 mdarade <mdarade@redhat.com> - 0.3.4-2
- Updated BuildRequires to contain libestr-devel

* Wed Aug  1 2012 Milan Bartos <mbartos@redhat.com> - 0.3.4-1
- initial port
