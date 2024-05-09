# Fedora Review: https://bugzilla.redhat.com/204954
Summary:        Open Fingerprint Architecture library
Name:           libofa
Version:        0.9.3
Release:        42%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://code.google.com/p/musicip-libofa/
# Source0:	https://musicip-libofa.googlecode.com/files/libofa-%{version}.tar.gz
Source0:        https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/musicip-libofa/libofa-%{version}.tar.gz
Patch1:         libofa-0.9.3-gcc41.patch
# Use Libs.private
Patch2:         libofa-0.9.3-pkgconfig.patch
Patch3:         libofa-0.9.3-gcc44.patch
Patch4:         libofa-0.9.3-curl.patch
Patch5:         libofa-0.9.3-gcc47.patch
# these are used only in the examples.
BuildRequires:  curl-devel
BuildRequires:  expat-devel
BuildRequires:  fftw-devel
BuildRequires:  findutils
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  sed

%description
Currently, MusicDNS and the Open Fingerprint Architecture are being used to:
* identify duplicate tracks, even when the metadata is different, MusicIP
  identifies the master recording.
* fix metadata
* find out more about tracks by connecting to MusicBrainz

%package devel
Summary:        Development headers and libraries for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# removed by patch2
#Requires: expat-devel fftw3-devel
%description devel
%{summary}.

%prep
%setup -q

find . -name README -or -name \*.cpp -or -name \*.h | xargs --no-run-if-empty sed -i -e 's|\r||'  ||:

%patch 1 -p1 -b .gcc41
%patch 2 -p1 -b .pkgconfig
%patch 3 -p1 -b .gcc43
%patch 4 -p1 -b .curl
%patch 5 -p1 -b .gcc47

## pkg-config < 0.20.0 (apparently?) doesn't grok URL
%if "%(pkg-config --version 2>/dev/null)" < "0.20.0"
#if 0%{?fedora} < 4 && 0%{?rhel} < 5
#if 0%{?rhel} == 4
sed -i -e "s|^URL:|#URL:|" *.pc.in ||:
%endif


%build
%configure --disable-static

%make_build


%install
%make_install

# unpackaged files
find %{buildroot} -type f -name "*.la" -delete -print

# prepare docs
make -C examples clean
rm -rf examples/.deps examples/Makefile examples/*.gcc43


%ldconfig_scriptlets

%files
%doc AUTHORS README
%license COPYING
%{_libdir}/libofa.so.0*

%files devel
%doc examples/
%{_includedir}/ofa1/
%{_libdir}/pkgconfig/libofa.pc
%{_libdir}/libofa.so

%changelog
* Mon Jan 16 2023 Suresh Thelkar <sthelkar@microsoft.com> - 0.9.3-42
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-33
- .spec cleanup
- BR: gcc-c++
- use %%license %%make_build %%make_install %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.3-26
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-20
- fix build against gcc47
- tighten %%files

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 01 2011 Than Ngo <than@redhat.com> - 0.9.3-18
- fix build failure against curl >= 7.21

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.9.3-15
- update Url, Source
- gcc44 patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-13
- multiarch conflicts (#342271)
- tweak gcc43

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> 0.9.3-12 
- gcc43 patch

* Sat Sep 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-11
- -devel: fix summary
- fix pkgconfig, URL-patching logic

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-10
- respin (BuildID)

* Sat Aug 11 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 0.9.3-9
- License: GPLv2

* Thu Sep 14 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-8
- better pkgconfig patch, using Libs.private

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-7
- fix rpmdoc handling

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-6
- de-DOS'ify .cpp, .h files too

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-5
- use sed instead of dos2unix
- omit examples/.deps

* Tue Sep 12 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-4
- remove extrenous entries from libofa.pc
- dos2unix README
- fix url in Source0
- -devel: %%doc examples/

* Mon Sep 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-3
- use gcc41 patch extracted from debian's patchset

* Mon Sep 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-2
- gcc41 patch

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.3-1
- first try
