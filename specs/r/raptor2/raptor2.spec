# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


Summary: RDF Parser Toolkit for Redland
Name:    raptor2
Version: 2.0.15
Release: 49%{?dist}

# Automatically converted from old format: GPLv2+ or LGPLv2+ or ASL 2.0 - review is highly recommended.
License: GPL-2.0-or-later OR LicenseRef-Callaway-LGPLv2+ OR Apache-2.0
Source:  http://download.librdf.org/source/raptor2-%{version}.tar.gz
URL:     http://librdf.org/raptor/

## upstream patches
# https://github.com/dajobe/raptor/commit/590681e546cd9aa18d57dc2ea1858cb734a3863f
Patch1: 0001-Calcualte-max-nspace-declarations-correctly-for-XML-.patch
# https://bugs.librdf.org/mantis/view.php?id=650
Patch2: 0001-CVE-2020-25713-raptor2-malformed-input-file-can-lead.patch

## upstreamable patches
Patch3: raptor2-configure-c99.patch
Patch4: raptor2-c99.patch
Patch5: raptor2-libxml2.patch

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: curl-devel
BuildRequires: gtk-doc
BuildRequires: libicu-devel
BuildRequires: pkgconfig(libxslt)
%if ! 0%{?rhel}
BuildRequires: yajl-devel
%endif

# when /usr/bin/rappor moved here  -- rex
Conflicts: raptor < 1.4.21-10

%description
Raptor is the RDF Parser Toolkit for Redland that provides
a set of standalone RDF parsers, generating triples from RDF/XML
or N-Triples.

%package devel
Summary: Development files for %{name} 
Requires: %{name}%{?_isa} = %{version}-%{release}
%description devel
%{summary}.


%prep
%autosetup -p1

# hack to nuke rpaths
%if "%{_libdir}" != "/usr/lib"
sed -i -e 's|"/lib /usr/lib|"/%{_lib} %{_libdir}|' configure
%endif


%build

%if 0%{?rhel}
%define distrooptions --with-yajl=no
%else
%define distrooptions --with-yajl=yes
%endif

%configure \
  --disable-static \
  --enable-release \
  --with-icu-config=/usr/bin/icu-config \
  %{distrooptions}

%make_build


%install
%make_install

## unpackaged files
rm -fv %{buildroot}%{_libdir}/lib*.la


%check
export PKG_CONFIG_PATH=%{buildroot}%{_datadir}/pkgconfig:%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion raptor2)" = "%{version}"
make check 


%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog NEWS README
%license COPYING* LICENSE.txt LICENSE-2.0.txt
%{_libdir}/libraptor2.so.0*
%{_bindir}/rapper
%{_mandir}/man1/rapper*

%files devel
%doc UPGRADING.html
%{_includedir}/raptor2/
%{_libdir}/libraptor2.so
%{_libdir}/pkgconfig/raptor2.pc
%{_mandir}/man3/libraptor2*
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html/
%{_datadir}/gtk-doc/html/raptor2/


%changelog
* Wed Aug 06 2025 František Zatloukal <fzatlouk@redhat.com> - 2.0.15-49
- Rebuilt for icu 77.1

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 08 2024 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-46
- Rebuild for ICU 76

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.15-45
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-43
- Rebuild for ICU 74

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Florian Weimer <fweimer@redhat.com> - 2.0.15-40
- Backport upstream patch to fix C compatibility issues
- Backport another upstream patch to fix build issue with current libxml2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 2.0.15-38
- Rebuilt for ICU 73.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-36
- Rebuild for ICU 72

* Thu Dec  8 2022 Florian Weimer <fweimer@redhat.com> - 2.0.15-35
- Port configure script to C99

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 2.0.15-34
- Rebuilt for ICU 71.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-30
- Rebuild for ICU 69

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-29
- Rebuild for ICU 69

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 11 2021 Caolán McNamara <caolanm@redhat.com> - 2.0.15-27
- Resolves: rhbz#1900686 CVE-2020-25713 malformed input file can lead to a segfault

* Mon Aug 10 2020 Caolán McNamara <caolanm@redhat.com> - 2.0.15-26
- Resolves: rhbz#1560206 drop requirement on yajl

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-25
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-23
- Rebuild for ICU 67

* Mon Feb 17 2020 Rex Dieter <rdieter@fedoraproject.org> - 2.0.15-22
- backport crash fix

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-20
- Rebuild for ICU 65

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-17
- Rebuild for ICU 63

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-15
- Rebuild for ICU 62

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-14
- Rebuild for ICU 61.1

* Wed Mar 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.0.15-13
- BR: gcc-c++, use %%make_build %%make_install %%license %%ldconfig_scriptlets

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 2.0.15-11
- Rebuild for ICU 60.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 2.0.15-7
- rebuild for ICU 57.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 2.0.15-5
- rebuild for ICU 56.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Rex Dieter <rdieter@fedoraproject.org> 2.0.15-3
- rebuild (gcc5)

* Mon Jan 26 2015 David Tardon <dtardon@redhat.com> - 2.0.15-2
- rebuild for ICU 54.1

* Mon Nov 03 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.15-1
- 2.0.15 (#1159636)

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 2.0.14-4
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 06 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.14-1
- 2.0.14 (#1094721)

* Tue Mar 04 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.13-1
- 2.0.13

* Wed Feb 12 2014 Rex Dieter <rdieter@fedoraproject.org> 2.0.9-3
- rebuild (libicu)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Mar 26 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.9-1
- 2.0.9
- BR: libicu-devel

* Tue Feb 19 2013 Rex Dieter <rdieter@fedoraproject.org> 2.0.8-1
- 2.0.8

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 23 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.7-1
- 2.0.7

* Mon Mar 05 2012 Rex Dieter <rdieter@fedoraproject.org> 2.0.6-1
- 2.0.6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-3
- rebuild (yajl)
- pkgconfig-style deps

* Sun Jul 31 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-2
- include rapper here

* Fri Jul 29 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.4-1
- 2.0.4

* Fri Jul 29 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-3
- upstream patch to fix build against newer libcurl

* Tue Jul 26 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-2
- -devel: drop Group: tag
- add lot's of %%doc's
- License: GPLv2+ or LGPLv2+ or ASL 2.0 (or newer)

* Sat Jul 23 2011 Rex Dieter <rdieter@fedoraproject.org> 2.0.3-1
- first try


