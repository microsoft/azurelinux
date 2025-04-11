Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		libotf
Version:	0.9.16
Release:	1%{?dist}
Summary:	A Library for handling OpenType Font

License:	LGPL-2.1-or-later
URL:            https://www.nongnu.org/m17n/
Source0:        https://download.savannah.gnu.org/releases/m17n/%{name}-%{version}.tar.gz

BuildRequires:	gcc chrpath freetype-devel
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
for file in $RPM_BUILD_ROOT%{bindir}/*; do chrpath -d $file || true; done

(cd example && make clean && rm -rf .deps && rm Makefile)
rm $RPM_BUILD_ROOT%{_bindir}/libotf-config

%ldconfig_scriptlets


%files
%doc AUTHORS COPYING README NEWS
%{_libdir}/*.so.1{,.*}
%{_bindir}/otfdump
%{_bindir}/otflist
%{_bindir}/otftobdf

%files devel
%doc example
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*

%changelog
* Thu Nov 21 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.9.16-1
- Upgrade to version 0.9.16

* Thu Mar 25 2021 Henry Li <lihl@microsoft.com> - 0.9.13-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove libXaw-devel from build requirement
- Remove otfview from file section, which depends on x11

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

