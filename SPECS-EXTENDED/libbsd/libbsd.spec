Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           libbsd
Version:        0.10.0
Release:        3%{?dist}
Summary:        Library providing BSD-compatible functions for portability
URL:            https://libbsd.freedesktop.org/
License:        BSD and ISC and Copyright only and Public Domain

Source0:        https://libbsd.freedesktop.org/releases/libbsd-%{version}.tar.xz
Patch1:         %{name}-0.8.3-deprecated.patch
Patch2:         %{name}-0.8.6-compat.patch

BuildRequires:  gcc
%description
libbsd provides useful functions commonly found on BSD systems, and
lacking on others like GNU systems, thus making it easier to port
projects with strong BSD origins, without needing to embed the same
code over and over again on each project.

%package devel
Summary:        Development files for libbsd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for the libbsd library.

%package ctor-static
Summary:        Development files for libbsd
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description ctor-static
The libbsd-ctor static library is required if setproctitle() is to be used
when libbsd is loaded via dlopen() from a threaded program.  This can be
configured using "pkg-config --libs libbsd-ctor".
# See the libbsd mailing list message by Guillem Jover on Jul 14 2013:
#     https://lists.freedesktop.org/archives/libbsd/2013-July/000091.html

%prep
%setup -q
%if 0%{?rhel} && 0%{?rhel} < 7
%patch 1 -p1 -b .deprecated
%patch 2 -p1 -b .compat
%endif

%build
%configure
%make_build V=1

%check
%make_build check V=1

%install
%make_install V=1

# don't want static library or libtool archive
rm %{buildroot}%{_libdir}/%{name}.a
rm %{buildroot}%{_libdir}/%{name}.la

# remove manual pages that conflict with man-pages package
rm %{buildroot}%{_mandir}/man3/explicit_bzero.3bsd


%ldconfig_scriptlets

%files
%license COPYING
%doc README TODO ChangeLog
%{_libdir}/%{name}.so.*

%files devel
%{_mandir}/man3/*.3bsd.*
%{_mandir}/man7/%{name}.7.*
%{_includedir}/bsd
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-overlay.pc

%files ctor-static
%{_libdir}/%{name}-ctor.a
%{_libdir}/pkgconfig/%{name}-ctor.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.10.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 22 2019 Eric Smith <brouhaha@fedoraproject.org> - 0.10.0-1
- Update to 0.10.1. (#1742611)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 22 2018 Eric Smith <brouhaha@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1. (#1538853)

* Tue May 22 2018 Eric Smith <brouhaha@fedoraproject.org> - 0.8.6-3
- Mark explicit_bzero() and reallocarray() as compat symbols. (#1408465)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 21 2017 Jens Petersen <petersen@redhat.com> - 0.8.6-1
- update to 0.8.6 (#1462722)
- fixes manpage conflict (#1504831)
- condition the gcc deprecation patch on epel < 7
- clean up spec file

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Eric Smith <brouhaha@fedoraproject.org> - 0.8.3-2
- Add patch for GCC deprecated attribute to allow building on GCC < 4.5
  (needed for EL5 and EL6).

* Thu Dec 22 2016 Eric Smith <brouhaha@fedoraproject.org> - 0.8.3-1
- Update to latest upstream release.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Eric Smith <brouhaha@fedoraproject.org> - 0.7.0-1
- Update to latest upstream release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Eric Smith <brouhaha@fedoraproject.org> - 0.6.0-1
- Update to latest upstream release. Remove patch 0.
- Added ctor-static subpackage.

* Sun Jul 07 2013 Eric Smith <brouhaha@fedoraproject.org> - 0.5.2-3
- Still having problems with setproctitle(), bug #981799, upstream
  freedesktop.org bug #66679. Added patch to noop out setproctitle().

* Tue Jun 11 2013 Eric Smith <brouhaha@fedoraproject.org> - 0.5.2-2
- Added check section.
- Add BuildRoot for EL5.

* Mon Jun 10 2013 Eric Smith <brouhaha@fedoraproject.org> - 0.5.2-1
- Update to latest upstream release. Remove patch 0.

* Thu Jun 06 2013 Eric Smith <brouhaha@fedoraproject.org> - 0.5.1-2
- Add patch to avoid calling clearenv() in setproctitle.c, bug #971513.

* Tue Jun 04 2013 Eric Smith <brouhaha@fedoraproject.org> - 0.5.1-1
- Update to latest upstream release.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 08 2012 Eric Smith <eric@brouhaha.com> - 0.4.2-1
- Update to latest upstream release.
- No longer need to change encoding of flopen(3) man page.

* Sun Jun 03 2012 Eric Smith <eric@brouhaha.com> - 0.4.1-1
- Update to latest upstream release.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 08 2011 Eric Smith <eric@brouhaha.com> - 0.3.0-1
- Update to latest upstream release.
- Removed Patch0, fixed upstream.
- Removed BuildRoot, clean, defattr.

* Fri Jan 29 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-3
- changes based on review by Sebastian Dziallas

* Fri Jan 29 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-2
- changes based on review comments by Jussi Lehtola and Ralf Corsepious

* Thu Jan 28 2010 Eric Smith <eric@brouhaha.com> - 0.2.0-1
- initial version
