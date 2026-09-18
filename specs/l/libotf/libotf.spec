# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		libotf
Version:	0.9.16
Release:	7%{?dist}
Summary:	A Library for handling OpenType Font

License:	LGPL-2.1-or-later
URL:            http://www.nongnu.org/m17n/
Source0:        http://download.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz

BuildRequires:	gcc chrpath freetype-devel libXaw-devel
BuildRequires: make
Requires:	freetype

%description 
The library "libotf" provides the following facilites.
Read Open Type Layout Tables from OTF file. Currently these tables are
supported; head, name, cmap, GDEF, GSUB, and GPOS.  Convert a Unicode
character sequence to a glyph code sequence by using the above tables.
The combination of libotf and the FreeType library (Ver.2) realizes
CTL (complex text layout) by OpenType fonts. This library is currently
used by the m17n library. It seems that the probject Free Type Layout
provides the similar (or better) facility as this library, but
currently they have not yet released their library. So, we have
developed this one.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}, pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
for file in $RPM_BUILD_ROOT%{_bindir}/*; do chrpath -d $file || true; done

(cd example && make clean && rm -rf .deps && rm Makefile)
rm $RPM_BUILD_ROOT%{_bindir}/libotf-config

%ldconfig_scriptlets


%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/libotf.so.1{,.*}
%{_bindir}/otfdump
%{_bindir}/otflist
%{_bindir}/otftobdf
%{_bindir}/otfview

%files devel
%doc example
%{_includedir}/*
%{_libdir}/libotf.so
%{_libdir}/pkgconfig/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.16-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 Lukáš Zaoral <lzaoral@redhat.com> - 0.9.16-2
- migrate to SPDX license format

* Tue Jul 25 2023 Mike FABIAN <mfabian@redhat.com> - 0.9.16-1
- Update to 0.9.16

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-17
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 18 2012 Parag Nemade <paragn AT fedoraproject DOT org> - 0.9.13-1
- Update to 0.9.13

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 06 2010 Parag Nemade <paragn AT fedoraproject.org> - 0.9.12-1
- Update to 0.9.12

* Wed May 19 2010 Neal Becker <ndbecker2@gmail.com> - 0.9.11-1
- Update to 0.9.11

* Sat Oct 24 2009 Neal Becker <ndbecker2@gmail.com> - 0.9.9-3
- Add BR libXaw-devel (BR 530586)

* Fri Oct  9 2009 Neal Becker <ndbecker2@gmail.com> - 0.9.9-2
- Remove libotf-config (just just pkg-config instead)
- Remove example/Makefile to fix multilib conflict

* Tue Aug 25 2009 Neal Becker <ndbecker2@gmail.com> - 0.9.9-1
- Update to 0.9.9

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Aug  8 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.8-1
- Update to 0.9.8

* Mon Apr 14 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-4
- Remove .deps from example

* Fri Mar 28 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-3
- Change to LGPLv2+
- Add examples

* Wed Mar 26 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-2
- Cleanup suggestions from panemade at gmail dot com

* Tue Mar 25 2008 Neal Becker <ndbecker2@gmail.com> - 0.9.7-1
- Initial

