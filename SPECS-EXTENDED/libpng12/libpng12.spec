Vendor:         Microsoft Corporation
Distribution:   Mariner
Summary: Old version of libpng, needed to run old binaries
Name: libpng12
Version: 1.2.57
Release: 16%{?dist}
License: zlib
URL: http://www.libpng.org/pub/png/

Source0: https://downloads.sourceforge.net/project/libpng/%{name}/older-releases/%{version}/libpng-%{version}.tar.xz#/%{name}-%{version}.tar.xz

Patch0: libpng12-multilib.patch
Patch1: libpng12-pngconf.patch

BuildRequires: gcc
BuildRequires: pkgconfig
BuildRequires: zlib-devel
BuildRequires: make

%description
The libpng12 package provides libpng 1.2, an older version of the libpng
library for manipulating PNG (Portable Network Graphics) image format files.
This version should be used only if you are unable to use the current
version of libpng.

%package devel
Summary: Development files for libpng 1.2
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: zlib-devel%{?_isa}

%description devel
The libpng12-devel package contains header files and documentation necessary
for developing programs using libpng12.

%prep
%autosetup -n libpng-%{version} -p1

%build
%configure \
  --disable-static \
  --without-libpng-compat

%make_build

%install
%make_install

## unpackaged files
# We don't ship .la files.
rm -fv $RPM_BUILD_ROOT%{_libdir}/libpng*.la
# drop man5 files, because these are in the base libpng package,
# which we don't want to conflict with.
rm -fv $RPM_BUILD_ROOT%{_mandir}/man5/*
# omit that conflicts with base libpng-devel package
rm -fv $RPM_BUILD_ROOT%{_bindir}/libpng-config
rm -fv $RPM_BUILD_ROOT%{_includedir}/{png,pngconf}.h
rm -fv $RPM_BUILD_ROOT%{_libdir}/libpng.so
rm -fv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/libpng.pc
rm -fv $RPM_BUILD_ROOT%{_mandir}/man3/{libpng,libpngpf}.3*

%check
make check

%files
%license LICENSE
%doc libpng-%{version}.txt README TODO CHANGES
%{_libdir}/libpng12.so.0*

%files devel
%{_bindir}/libpng12-config
%{_includedir}/libpng12/
%{_libdir}/libpng12.so
%{_libdir}/pkgconfig/libpng12.pc

%changelog
* Thu Mar 09 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 1.2.57-16
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Nikola Forró <nforro@redhat.com> - 1.2.57-7
- Remove ldconfig from scriptlets

* Tue Feb 20 2018 Nikola Forró <nforro@redhat.com> - 1.2.57-6
- Add missing gcc build dependency

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.57-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Nikola Forró <nforro@redhat.com> - 1.2.57-2
- Update source URL (#1459085)

* Tue Apr 04 2017 Nikola Forró <nforro@redhat.com> - 1.2.57-1
- New upstream release 1.2.57

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Rex Dieter <rdieter@fedoraproject.org> 1.2.56-1
- 1.2.56 release, .spec cosmetics, add (minimalist) 'make check'

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 28 2014 Petr Hracek <phracek@redhat.com> - 1.2.50-6
- Adding CVE-2013-6954 patch

* Sun Aug 18 2013 Rex Dieter <rdieter@fedoraproject.org> - 1.2.50-5
- devel: fix so we can drop Conflicts: libpng-devel
- drop libpng-compat stuff

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012 Tom Lane <tgl@redhat.com> 1.2.50-2
- Remove unnecessary use of epoch
Related: #850628

* Fri Aug  3 2012 Tom Lane <tgl@redhat.com> 1.2.50-1
- Update to 1.2.50 (just on general principles)
- Add Obsoletes: libpng-compat

* Wed Aug  1 2012 Tom Lane <tgl@redhat.com> 1.2.49-1
- Created from libpng
