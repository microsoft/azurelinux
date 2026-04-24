# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} || 0%{?rhel} >= 9
%global blaslib flexiblas
%else
%global blaslib openblas
%endif

Name:		qrupdate
Version:	1.1.2
Release: 35%{?dist}
Summary:	A Fortran library for fast updates of QR and Cholesky decompositions
# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:	GPL-3.0-or-later
URL:		http://qrupdate.sourceforge.net/
Source0:	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

BuildRequires: make
BuildRequires:	gcc-gfortran

BuildRequires:	%{blaslib}-devel

%description
qrupdate is a Fortran library for fast updates of QR and Cholesky
decompositions. 

%package devel
Summary:	Development libraries for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	%{blaslib}-devel%{?_isa}

%description devel
This package contains the development libraries for %{name}.

%prep
%setup -q
# Modify install location
sed -i 's|$(PREFIX)/lib/|$(DESTDIR)%{_libdir}/|g' src/Makefile

%build
%make_build solib FC=gfortran FFLAGS="%{optflags} -fimplicit-none -funroll-loops -fallow-argument-mismatch $LDFLAGS" BLAS="-l%{blaslib}" LAPACK=

%install
make install-shlib LIBDIR=%{_libdir} PREFIX="%{buildroot}"
# Verify attributes
chmod 755 %{buildroot}%{_libdir}/libqrupdate.*

%check
make test FC=gfortran FFLAGS="%{optflags} -fimplicit-none -funroll-loops -fallow-argument-mismatch $LDFLAGS" BLAS="-l%{blaslib}" LAPACK=

%ldconfig_scriptlets

%files
%license COPYING
%doc README ChangeLog
%{_libdir}/libqrupdate.so.*

%files devel
%{_libdir}/libqrupdate.so


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Orion Poplawski <orion@nwra.com> - 1.1.2-33
- Build with flexiblas on EL9+ (bz#2257317)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 1.1.2-31
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 16 2020 Iñaki Úcar <iucar@fedoraproject.org> - 1.1.2-21
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Mar 10 2019 Orion Poplawski <orion@nwra.com> - 1.1.2-17
- Use openblas

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Jitka Plesnikova <jplesnik@redhat.com> - 1.1.2-13
- Rebuild for new gfortran

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 1.1.2-9
- Rebuild for gcc 7
- Cleanup spec

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 07 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 12 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1.

* Mon Jan 11 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.0-2
- Bump spec.

* Mon Jan 11 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 1.0.1-1
- First release.
