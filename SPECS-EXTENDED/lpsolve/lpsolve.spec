Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:      lpsolve
Summary:   A Mixed Integer Linear Programming (MILP) solver
Version:   5.5.2.0
Release:   26%{?dist}
Source:    http://downloads.sourceforge.net/lpsolve/lp_solve_%{version}_source.tar.gz
URL:       http://sourceforge.net/projects/lpsolve
License:   LGPLv2+

BuildRequires: gcc-c++

Patch0:    lpsolve-5.5.0.11.cflags.patch
Patch1:    lpsolve-5.5.2.0.defines.patch

%description
Mixed Integer Linear Programming (MILP) solver lpsolve solves pure linear,
(mixed) integer/binary, semi-continuous and special ordered sets (SOS) models.

%package devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Summary: Files for developing with lpsolve

%description devel
Includes and definitions for developing with lpsolve 

%prep
%setup -q -n lp_solve_5.5
%patch0 -p1 -b .cflags.patch
%patch1 -p1 -b .defines.patch

%build
%set_build_flags
cd lpsolve55
sh -x ccc
rm bin/ux*/liblpsolve55.a
cd ../lp_solve
sh -x ccc

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir} $RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_includedir}/lpsolve
install -p -m 755 \
        lp_solve/bin/ux*/lp_solve $RPM_BUILD_ROOT%{_bindir}
install -p -m 755 \
        lpsolve55/bin/ux*/liblpsolve55.so $RPM_BUILD_ROOT%{_libdir}
install -p -m 644 \
        lp*.h $RPM_BUILD_ROOT%{_includedir}/lpsolve

%ldconfig_scriptlets

%files
%license bfp/bfp_LUSOL/LUSOL/LUSOL_LGPL.txt
%doc README.txt ./bfp/bfp_LUSOL/LUSOL/LUSOL_README.txt ./bfp/bfp_LUSOL/LUSOL/LUSOL-overview.txt
%{_bindir}/lp_solve
%{_libdir}/*.so

%files devel
%{_includedir}/lpsolve

%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 5.5.2.0-26
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.5.2.0-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 26 2018 Caolán McNamara <caolanm@redhat.com> - 5.5.2.0-20
- Related: rhbz#1548689 ... and LDFLAGS

* Mon Feb 26 2018 Caolán McNamara <caolanm@redhat.com> - 5.5.2.0-19
- Related: rhbz#1548689 there are two build scripts that need adjusting

* Mon Feb 26 2018 Caolán McNamara <caolanm@redhat.com> - 5.5.2.0-18
- Resolves: rhbz#1548689 use fedora compile/link flags

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 15 2016 Caolán McNamara <caolanm@redhat.com> - 5.5.2.0-13
- Resolves: rhbz#1307751 FTBFS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 17 2014 Caolán McNamara <caolanm@redhat.com> - 5.5.2.0-9
- Resolves: rhbz#1109265 lpsolve.i686 missing in x86_64 repo

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Dan Horák <dan[at]danny.cz> - 5.5.2.0-2
- fix build on s390(x)

* Fri Aug 13 2010 Caolán McNamara <caolanm@redhat.com> - 5.5.2.0-1
- latest version

* Mon Dec 21 2009 Caolán McNamara <caolanm@redhat.com> - 5.5.0.15-3
- Preserve timestamps

* Thu Nov 05 2009 Caolán McNamara <caolanm@redhat.com> - 5.5.0.15-2
- upstream source silently changed content

* Sat Sep 12 2009 Caolán McNamara <caolanm@redhat.com> - 5.5.0.15-1
- latest version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.5.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Caolán McNamara <caolanm@redhat.com> - 5.5.0.14-2
- defuzz patch

* Mon Feb 02 2009 Caolán McNamara <caolanm@redhat.com> - 5.5.0.14-1
- latest version

* Fri Jan 02 2009 Dennis Gilmore <dennis@ausil.us> - 5.5.0.13-2
- use -fPIC on sparc and s390 arches

* Mon Aug 04 2008 Caolán McNamara <caolanm@redhat.com> - 5.5.0.13-1
- latest version

* Sat Aug 02 2008 Caolán McNamara <caolanm@redhat.com> - 5.5.0.12-2
- Mar 20 upstream tarball now differs from Mar 14 tarball

* Fri Mar 14 2008 Caolán McNamara <caolanm@redhat.com> - 5.5.0.12-1
- latest version

* Wed Feb 20 2008 Caolán McNamara <caolanm@redhat.com> - 5.5.0.11-1
- initial version
