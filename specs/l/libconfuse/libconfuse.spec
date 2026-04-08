# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libconfuse
Version:        3.3
Release:        15%{?dist}
Summary:        A configuration file parser library

License:        ISC
URL:            https://github.com/martinh/libconfuse
Source0:	https://github.com/martinh/libconfuse/releases/download/v%{version}/confuse-%{version}.tar.gz

Patch0:         d73777c2c3566fb2647727bb56d9a2295b81669b.patch

BuildRequires:  gcc
BuildRequires:  check-devel, pkgconfig
BuildRequires:  perl-interpreter
BuildRequires: make

%description
libConfuse is a configuration file parser library, licensed under
the terms of the ISC license, and written in C. It supports
sections and (lists of) values (strings, integers, floats,
booleans or other sections), as well as some other features (such
as single/double-quoted strings, environment variable expansion,
functions and nested include statements). It makes it very
easy to add configuration file capability to a program using
a simple API.

The goal of libConfuse is not to be the configuration file parser
library with a gazillion of features. Instead, it aims to be
easy to use and quick to integrate with your code.

%package devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig

%description devel
Development files for %{name}.


%prep
%setup -q -n confuse-%{version}
perl -pi.orig -e 's|confuse.h|../src/confuse.h|g' tests/check_confuse.c

%patch -P0 -p0

%build
%configure --enable-shared --disable-static
make %{?_smp_mflags} AM_CFLAGS="-Wall -Wextra"

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT
# Nuke libtool archive(s)
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
# Install man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man3/
cp -p doc/man/man3/*.3 $RPM_BUILD_ROOT%{_mandir}/man3/
# Extract the example sources
mkdir -p ex2/examples
cp -p examples/{ftpconf.c,ftp.conf,simple.c,simple.conf,reread.c,reread.conf} \
    ex2/examples/

#Remove spurious docs
rm -rf $RPM_BUILD_ROOT%{_datadir}/doc/confuse

%find_lang confuse


%ldconfig_scriptlets


%files -f confuse.lang
%license LICENSE
%doc AUTHORS README.md
%doc doc/html
%{_libdir}/libconfuse.so.2*
%{_mandir}/man?/*.*

%files devel
%doc ex2/examples
%{_includedir}/confuse.h
%{_libdir}/libconfuse.so
%{_libdir}/pkgconfig/libconfuse.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 3.3-9
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 12 2022 Gwyn Ciesla <gwync@protonmail.com> - 3.3-7
- Patch for CVE-2022-40320

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Gwyn Ciesla <gwync@protonmail.com> - 3.3-1
- 3.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Gwyn Ciesla <limburgher@gmail.com> - 3.2.2-1
- 3.2.2, fix for CVE-2018-14447.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Aug 18 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.2.1-1
- 3.2.1, BZ 1482712

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.2-1
- 3.2, BZ 1458525

* Thu May 25 2017 Gwyn Ciesla <limburgher@gmail.com> - 3.1-1
- 3.1, BZ 1455367

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jun 14 2016 Jon Ciesla <limburgher@gmail.com> - 3.0-1
- New upstream URL, latest release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Jon Ciesla <limb@jcomserv.net> - 2.7-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 04 2008 Jarod Wilson <jwilson@redhat.com> 2.6-1
- New upstream release
- Switch from LGPL to ISC license
- Build fix from Hans Ulrich Niedermann

* Tue Sep 05 2006 Jarod Wilson <jwilson@redaht.com> 2.5-3
- Rebuild for new glibc

* Wed Aug 16 2006 Jarod Wilson <jwilson@redhat.com> 2.5-2
- Put -devel package in the right Group
- Add defattr for -devel files

* Wed Aug 16 2006 Jarod Wilson <jwilson@redhat.com> 2.5-1
- Initial build
