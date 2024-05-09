Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libsigc++20
Version:        2.10.3
Release:        2%{?dist}
Summary:        Typesafe signal framework for C++

License:        LGPLv2+
URL:            https://libsigc.sourceforge.net/
Source0:        https://download.gnome.org/sources/libsigc++/%{release_version}/libsigc++-%{version}.tar.xz

BuildRequires:  gcc-c++
BuildRequires:  m4
BuildRequires:  perl-interpreter
BuildRequires:  perl(Getopt::Long)

%description
libsigc++ implements a typesafe callback system for standard C++. It
allows you to define signals and to connect those signals to any
callback function, either global or a member function, regardless of
whether it is static or virtual.

libsigc++ is used by gtkmm to wrap the GTK+ signal system. It does not
depend on GTK+ or gtkmm.


%package devel
Summary:        Development tools for the typesafe signal framework for C++
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the static libraries and header files
needed for development with %{name}.


%package        doc
Summary:        Documentation for %{name}, includes full API docs
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.


%prep
%setup -q -n libsigc++-%{version}


%build
%configure
make %{?_smp_mflags}


%install
%make_install
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'


%files
%license COPYING
%doc AUTHORS README NEWS
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/sigc++-2.0/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%files doc
%doc %{_datadir}/doc/libsigc++-2.0/
# according guidelines, we can co-own this, since devhelp is not required
# for accessing documentation
%doc %{_datadir}/devhelp/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.10.3-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 2.10.3-1
- Update to 2.10.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 12 2019 Kalev Lember <klember@redhat.com> - 2.10.2-1
- Update to 2.10.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 31 2018 Kalev Lember <klember@redhat.com> - 2.10.1-1
- Update to 2.10.1
- Remove ldconfig scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com> - 2.10.0-1
- Update to 2.10.0
- Don't set group tags
- Use make_install macro

* Mon Jul 18 2016 Kalev Lember <klember@redhat.com> - 2.9.3-1
- Update to 2.9.3

* Wed Mar 16 2016 Kalev Lember <klember@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Fri Mar 11 2016 Kalev Lember <klember@redhat.com> - 2.7.2-1
- Update to 2.7.2

* Fri Mar 04 2016 Kalev Lember <klember@redhat.com> - 2.7.1-1
- Update to 2.7.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Kalev Lember <klember@redhat.com> - 2.6.2-1
- Update to 2.6.2

* Sat Sep 26 2015 Kalev Lember <klember@redhat.com> - 2.6.1-1
- Update to 2.6.1

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 2.6.0-1
- Update to 2.6.0
- Use license macro for COPYING

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.4.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Mon Sep 15 2014 Kalev Lember <kalevlember@gmail.com> - 2.4.0-1
- Update to 2.4.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Kalev Lember <kalevlember@gmail.com> - 2.3.2-1
- Update to 2.3.2
- Don't include huge ChangeLog file
- Tighten deps with the _isa macro

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 24 2012 Kalev Lember <kalevlember@gmail.com> - 2.3.1-1
- Update to 2.3.1

* Sun Sep 23 2012 Kalev Lember <kalevlember@gmail.com> - 2.2.11-1
- Update to 2.2.11

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Kalev Lember <kalevlember@gmail.com> - 2.2.10-1
- Update to 2.2.10
- Cleaned up the spec file for modern rpmbuild

* Wed Mar 09 2011 Kalev Lember <kalev@smartlink.ee> - 2.2.9-1
- Update to 2.2.9
- Dropped upstreamed libsigc++20-gcc46.patch

* Tue Mar 01 2011 Kalev Lember <kalev@smartlink.ee> - 2.2.8-4
- Spec cleanup
- Use macro for automatically calculating ftp directory name with
  first two digits of tarball version.
- Dropped R: pkgconfig from -devel as it's now automatically added by rpm
- Own /usr/share/doc/libsigc++-2.0/ dir and mark /usr/share/devhelp/ as %%doc
- Require base package from -doc subpackage
- Drop unneeded doxygen and graphviz BRs

* Mon Feb 21 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.2.8-3
- fix documentation location (RHBZ #678981)
- co-own /usr/share/devhelp

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb  4 2011 Haïkel Guémar <hguemar@fedoraproject.org> - 2.2.8-1
- upstream 2.2.8
- fix compilation against GCC 4.6 (GNOME BZ #641471)

* Tue Sep  8 2009 Denis Leroy <denis@poolshark.org> - 2.2.4.2-1
- Update to upstream version 2.2.4.2

* Sat Aug 29 2009 Denis Leroy <denis@poolshark.org> - 2.2.4.1-1
- Update to upstream 2.2.4.1
- Added devhelp book and necessary BRs
- Split documentation into new subpackage
- Moved documentation to gtk-doc dir

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 2.2.2-2
- Rebuild for pkgconfig provides

* Tue Mar 11 2008 Denis Leroy <denis@poolshark.org> - 2.2.2-1
- Update to upstream 2.2.2 version

* Sun Feb 24 2008 Denis Leroy <denis@poolshark.org> - 2.2.0-1
- Update to 2.2.0
- gcc 4.3 patch upstreamed

* Thu Feb  7 2008 Lubomir Kundrak <lkundrak@redhat.com> 2.0.18-3
- Rebuild with gcc4.3

* Thu Jan  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.18-2
- add test case for gcc4.3 failure conditional

* Fri Sep 14 2007 Denis Leroy <denis@poolshark.org> - 2.0.18-1
- Update to 2.0.18

* Fri Aug 10 2007 Denis Leroy <denis@poolshark.org> - 2.0.17-3
- Updated License tag as per new guidelines

* Mon Aug 28 2006 Denis Leroy <denis@poolshark.org> - 2.0.17-2
- FE6 Rebuild

* Tue Feb 28 2006 Denis Leroy <denis@poolshark.org> - 2.0.17-1
- Upgrade to version 2.0.17
- Added optional macro to compile static libs (use '--with static')

* Fri Nov 25 2005 Denis Leroy <denis@poolshark.org> - 2.0.16-2
- Disabled static libraries
- Was missing copy of GPL licence

* Sun Sep 18 2005 Denis Leroy <denis@poolshark.org> - 2.0.16-1
- Upgrade to version 2.0.16

* Sat Apr  9 2005 Denis Leroy <denis@poolshark.org> - 2.0.11-1
- Upgrade to version 2.0.11

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Jan 15 2005 Rick L Vinyard Jr <rvinyard@cs.nmsu.edu> - 0:2.0.6-1
- Update to 2.0.6

* Sun Jun 27 2004 Denis Leroy <denis@poolshark.org> - 0:2.0.3-0.fdr.1
- Update to 2.0.3
- Merged deps from FC2 sigc++ 1.2.5 spec
- Moved docs to regular directory

* Sat Apr 15 2000 Dmitry V. Levin <ldv@fandra.org>
- updated Url and Source fileds
- 1.0.0 stable release

* Sat Jan 22 2000 Dmitry V. Levin <ldv@fandra.org>
- filtering out -fno-rtti and -fno-exceptions options from $RPM_OPT_FLAGS
- minor install section cleanup

* Wed Jan 19 2000 Allan Rae <rae@lyx.org>
- autogen just creates configure, not runs it, so cleaned that up too.

* Wed Jan 19 2000 Dmitry V. Levin <ldv@fandra.org>
- minor attr fix
- removed unnecessary curly braces
- fixed Herbert's adjustement

* Sat Jan 15 2000 Dmitry V. Levin <ldv@fandra.org>
- minor package dependence fix

* Sat Dec 25 1999 Herbert Valerio Riedel <hvr@gnu.org>
- fixed typo of mine
- added traditional CUSTOM_RELEASE stuff
- added SMP support

* Thu Dec 23 1999 Herbert Valerio Riedel <hvr@gnu.org>
- adjusted spec file to get tests.Makefile and examples.Makefile from scripts/

* Fri Oct 22 1999 Dmitry V. Levin <ldv@fandra.org>
- split into three packages: libsigc++, libsigc++-devel and libsigc++-examples

* Thu Aug 12 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- updated source field and merged conflicts between revisions.

* Tue Aug 10 1999 Dmitry V. Levin <ldv@fandra.org>
- updated Prefix and BuildRoot fields

* Thu Aug  5 1999 Herbert Valerio Riedel <hvr@hvrlab.dhs.org>
- made sure configure works on all alphas

* Wed Jul  7 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- Added autoconf macro for sigc.

* Fri Jun 11 1999 Karl Nelson <kenelson@ece.ucdavis.edu>
- Made into a .in to keep version field up to date
- Still need to do release by hand

* Mon Jun  7 1999 Dmitry V. Levin <ldv@fandra.org>
- added Vendor and Packager fields

* Sat Jun  5 1999 Dmitry V. Levin <ldv@fandra.org>
- updated to 0.8.0

* Tue Jun  1 1999 Dmitry V. Levin <ldv@fandra.org>
- initial revision
