Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           liblqr-1
Version:        0.4.2
Release:        15%{?dist}
Summary:        LiquidRescale library
License:        GPLv3
URL:            https://liquidrescale.wikidot.com/
Source0:        https://liblqr.wikidot.com/local--files/en:download-page/%{name}-%{version}.tar.bz2
BuildRequires:  gcc
BuildRequires:  glib2-devel

%description
The LiquidRescale (lqr) library provides a C/C++ API for
performing non-uniform resizing of images by the seam-carving
technique.

%package devel
Summary:        LiquidRescale library  development kit
License:        GPLv3
Requires:       %{name} = %{version}-%{release}
Requires:       glib2-devel, pkgconfig

%description devel
The libqr-devel package contains the header files
needed to develop applications with liblqr

%prep
%setup -q

%build
export LDFLAGS="`pkg-config --libs glib-2.0` -lm"
%configure
%{__make} %{?_smp_mflags}

%install
%{__make} install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

# remove .la files
find $RPM_BUILD_ROOT -name \*.la -exec %{__rm} -f {} \;

# Fedora MUST
%ldconfig_scriptlets

%files 
%doc README ChangeLog COPYING
%{_libdir}/liblqr-1.so.0.3.2
%{_libdir}/liblqr-1.so.0

%files devel
%doc docs/liblqr_manual.docbook
%{_libdir}/liblqr-1.so
%{_includedir}/lqr-1/
%{_libdir}/pkgconfig/lqr-1.pc


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4.2-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Feb 16 2013 Sven Lankes <sven@lank.es> - 0.4.2-1
- Update to latest upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Aug 03 2009 Sven Lankes <sven@lank.es> - 0.4.1-1
- Update to latest upstream release
- Remove upstreamed patch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.1.0-6
- Fix Patch0:/%%patch mismatch.

* Fri Feb 29 2008 Alexandru Ciobanu <alex@tvtransilvania.ro> - 0.1.0-5
- Applied pkgconfig patch to remove unneeded directories.
- Changed permissions of files to 0644.
- Fixed minor typos.

* Mon Feb 25 2008 Alexandru Ciobanu <alex@tvtransilvania.ro> - 0.1.0-4
- Cleaned SPEC file, again.

* Wed Feb 20 2008 Alexandru Ciobanu <alex@tvtransilvania.ro> - 0.1.0-3
- Cleaned SPEC file.

* Tue Feb 19 2008 Alexandru Ciobanu <alex@tvtransilvania.ro> - 0.1.0-2
- Fixed licensing issue.

* Thu Jan 17 2008 Alexandru Ciobanu <alex@tvtransilvania.ro> - 0.1.0-1
- Update to latest upstream release.
- Added glib BuildRequires.

* Mon Dec 10 2007 Alexandru Ciobanu <alex@tvtransilvania.ro> - 0.1.0-0
- Initial RPM release.
