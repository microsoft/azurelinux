Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libuninameslist
Version:        20230916
Release:        5%{?dist}

Summary:        A library providing Unicode character names and annotations

License:        BSD
URL:            https://github.com/fontforge/libuninameslist
Source0:        https://github.com/fontforge/libuninameslist/archive/%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires: make

%description
libuninameslist provides applications with access to Unicode name and
annotation data from the official Unicode Character Database.

%package        devel
Summary:        Header files and static libraries for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
This package contains header files and static libraries for %{name}.


%prep
%autosetup

%build
autoreconf -i
automake --foreign -Wall
%configure --disable-static
make V=1 %{?_smp_mflags}


%install
%make_install incdir=$RPM_BUILD_ROOT%{_includedir}
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

%files
%license LICENSE
%doc ChangeLog README.md
%{_libdir}/*.so.*

%files devel
%{_mandir}/man3/libuninameslist.3.gz
%{_libdir}/*.so
%{_includedir}/*
%{_libdir}/pkgconfig/libuninameslist.pc

%changelog
* Fri Nov 15 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 20230916-5
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230916-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230916-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20230916-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 18 2023 Parag Nemade <pnemade AT redhat DOT com> - 20230916-1
- Update to 20230916 version (#2239363)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20230523-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 23 2023 Parag Nemade <pnemade AT redhat DOT com> - 20230523-2
- Migrate to SPDX license expression

* Tue May 30 2023 Parag Nemade <pnemade AT redhat DOT com> - 20230523-1
- Update to 20230523 version (#2209761)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20221022-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Parag Nemade <pnemade AT redhat DOT com> - 20221022-1
- Update to 20221022 version (#2137768)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20220701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 04 2022 Parag Nemade <pnemade AT redhat DOT com> - 20220701-1
- Update to 20220701 version (#2103354)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20211114-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Parag Nemade <pnemade AT redhat DOT com> - 20211114-1
- Update to 20211114 version (#2023054)

* Tue Sep 28 2021 Parag Nemade <pnemade AT redhat DOT com> - 20210917-1
- Update to 20210917 version (#2005533)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210626-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul 02 2021 Parag Nemade <pnemade AT redhat DOT com> - 20210626-1
- Update to 20210626 version (#1976540)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200413-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200413-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Apr 15 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200413-1
- Update to 20200413 version (#1823434)

* Wed Mar 25 2020 Parag Nemade <pnemade AT redhat DOT com> - 20200313-1
- Update to 20200313 version (#1813493)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190701-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 05 2019 Kevin Fenzi <kevin@scrye.com> - 20190701-1
- Update to 20190701. Fixes bug #1725748

* Sun Mar 10 2019 Kevin Fenzi <kevin@scrye.com> - 20190305-1
- Update to 20190305. Fixes bug #1685821

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180701-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Parag Nemade <pnemade AT redhat DOT com> - 20180701-1
- Update to 20180701 version (#1564872)

* Fri Jun 22 2018 Parag Nemade <pnemade AT redhat DOT com> - 20180408-1
- Update to 20180408 version (#1564872)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170701-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170701-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 02 2017 Parag Nemade <pnemade AT redhat DOT com> - 20170701-1
- Update to 20170701 version

* Sat Jun 10 2017 Parag Nemade <pnemade AT redhat DOT com> - 20170319-1
- Update to 20170319 version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20160701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 05 2016 Kevin Fenzi <kevin@scrye.com> - 20160701-1
- Update to 20160701. Fixes bug #1352498

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20150701-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 08 2015 Kevin Fenzi <kevin@scrye.com> - 20150701-1
- Update to 0.5 / 20150701. Fixes bug #1278628

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130501-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130501-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130501-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Dec 03 2013 Kevin Fenzi <kevin@scrye.com> 20130501-1
- Update to 20130501

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091231-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 23 2013 Kevin Fenzi <kevin@scrye.com> 20091231-6
- Add patch to support aarch64. Fixes bug #925910

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091231-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091231-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091231-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20091231-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 16 2010 Kevin Fenzi <kevin@tummy.com> - 20091231-1
- Update to 20091231
- Do not ship static libs - bug #556078

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080409-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080409-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan 15 2009 Roozbeh Pournader <roozbeh@gmail.com> - 20080409-1
- Update to upstream 20080409: Unicode 5.1 support
- Change package versioning scheme
- Update summary and description
- Add DistTag
- Remove copy of GPL from RPM: the only file it applies to is not shipped

* Sun Feb 10 2008 Kevin Fenzi <kevin@tummy.com> - 0.0-8.20060907
- Rebuild for gcc43

* Sun Aug 26 2007 Kevin Fenzi <kevin@tummy.com> - 0.0-7.20060907
- Rebuild for BuildID

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.0-6.20060907
 - rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Wed Sep 20 2006 Kevin Fenzi <kevin@tummy.com> - 0.0-5.20060907
- Take over maintainership. 
- Update to 20060907

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 0.0-4.040707
- rebuild on all arches

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jul 17 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.2.040707
- Updated to 040707.

* Fri Jul  2 2004 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.2.040701
- Updated to 040701.

* Mon Oct 13 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:0.0-0.fdr.2.030713
- Enable static libs, add -devel subpackage.

* Mon Oct 13 2003 Marius L. Jøhndal <mariuslj at ifi.uio.no> - 0:0.0-0.fdr.1.030713
- Initial RPM release.
