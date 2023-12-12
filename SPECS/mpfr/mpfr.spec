Summary:        Functions for multiple precision math
Name:           mpfr
Version:        4.1.0
Release:        2%{?dist}
License:        GPLv3+
URL:            http://www.mpfr.org
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://www.mpfr.org/%{name}-%{version}/%{name}-%{version}.tar.xz
Requires:       gmp

%description
The MPFR package contains functions for multiple precision math.

%package    devel
Summary:    Header and development files for mpfr
Requires:   %{name} = %{version}

%description    devel
It contains the libraries and header files to create applications

%prep
%setup -q
%build
./configure \
    --prefix=%{_prefix} \
    --enable-thread-safe \
    --docdir=%{_defaultdocdir}/%{name}-%{version} \
    --disable-silent-rules
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot}%{_libdir} -name '*.la' -delete
rm -rf %{buildroot}%{_infodir}

%check
make %{?_smp_mflags} check

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/libmpfr.so.*

%files devel
%{_includedir}/mpf2mpfr.h
%{_includedir}/mpfr.h
%{_libdir}/libmpfr.a
%{_libdir}/libmpfr.so
%{_libdir}/pkgconfig/*
%{_docdir}/mpfr-%{version}/NEWS
%{_docdir}/mpfr-%{version}/FAQ.html
%{_docdir}/mpfr-%{version}/examples/version.c
%{_docdir}/mpfr-%{version}/examples/rndo-add.c
%{_docdir}/mpfr-%{version}/examples/ReadMe
%{_docdir}/mpfr-%{version}/examples/sample.c
%{_docdir}/mpfr-%{version}/examples/divworst.c
%{_docdir}/mpfr-%{version}/examples/can_round.c
%{_docdir}/mpfr-%{version}/examples/threads.c
%{_docdir}/mpfr-%{version}/COPYING.LESSER
%{_docdir}/mpfr-%{version}/TODO
%{_docdir}/mpfr-%{version}/BUGS
%{_docdir}/mpfr-%{version}/AUTHORS
%{_docdir}/mpfr-%{version}/COPYING

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 4.1.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Oct 11 2021 Andrew Phelps <anphel@microsoft.com> - 4.1.0-1
- Update to version 4.1.0
- License verified.
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.0.1-3
- Added %%license line automatically
* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 4.0.1-2
- Initial CBL-Mariner import from Photon (license: Apache2).
* Thu Sep 20 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 4.0.1-1
- Update package version
* Fri Mar 31 2017 Michelle Wang <michellew@vmware.com> 3.1.5-1
- Update package version
* Mon Oct 03 2016 ChangLee <changlee@vmware.com> 3.1.3-3
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.1.3-2
- GA - Bump release of all rpms
* Tue Jan 12 2016 Anish Swaminathan <anishs@vmware.com>  3.1.3-1
- Update version.
* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com>> 3.1.2-1
- Initial build. First version
