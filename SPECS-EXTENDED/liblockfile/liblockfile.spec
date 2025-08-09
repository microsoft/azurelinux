Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           liblockfile
Version:        1.17
Release:        1%{?dist}
Summary:        This implements a number of functions found in -lmail on SysV systems

# regarding license please see file COPYRIGHT
License:        GPLv2+ and LGPLv2+
URL:            http://packages.qa.debian.org/libl/liblockfile.html
Source0:        https://github.com/miquels/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc

%description
This library implements a number of functions found in -lmail on SysV
systems. These functions are designed to lock the standard mailboxes in
/var/mail (or wherever the system puts them).

In additions, this library adds a number of functions to create,
manage and remove generic lockfiles.

%package devel
Summary: Development files for %{name}
Requires: %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}

# remove -g root from install
sed -i "s/-g root//" Makefile.in


%build
%configure --enable-shared --prefix=%{buildroot} --bindir=%{buildroot}%{_bindir} --mandir=%{buildroot}%{_mandir} --libdir=%{buildroot}%{_libdir} --includedir=%{buildroot}%{_includedir}
make


%install
export DESTDIR=%{buildroot}
make install

ldconfig -N -n %{buildroot}/%{_libdir}


%ldconfig_scriptlets


%files
%{_bindir}/dotlockfile
%{_libdir}/liblockfile.so.1.0
%{_libdir}/liblockfile.so.1
%{_mandir}/man1/dotlockfile.1*
%doc README COPYRIGHT Changelog


%files devel
%{_libdir}/liblockfile.so
%{_includedir}/maillock.h
%{_includedir}/lockfile.h
%{_libdir}/liblockfile.a
%{_mandir}/man3/lockfile_create.3*
%{_mandir}/man3/maillock.3*


%changelog
* Thu Nov 07 2021 Kevin Lockwood <v-klockwood@microsoft.com> - 1.17-1
- Update to 1.17
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 Matthias Runge <mrunge@redhat.com> - 1.14-1
- update to 1.14 (rhbz#1548753)
- fixed build flags injection (rhbz#1548706)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.09-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.09-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 15 2015 Matthias Runge <mrunge@redhat.com> - 1.09-1
- update to 1.09
- resolve timeout issue (rhbz#1159377)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Sep 14 2012 Matthias Runge <mrunge@redhat.com> - 1.08-14
- license is GPLv2+ and LGPLv2+
- minor spec cleanups

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.08-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Aug 14 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08.10
- replace linking of libs with ldconfig

* Fri Aug 6 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-9
- change description and summary of -devel-subpackage
- make wildcard for man-pages even match against uncompressed files

* Fri Aug 6 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-8
- rename to liblockfile
- sorting file to main and -devel package
- explicitly list files in files-section

* Fri Aug 6 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-7
- remove COPYRIGHT from devel
- just fix one missing link from upstream

* Thu Aug 5 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-6
- include COPYRIGHT in -devel, too
- remove unnecessary exclude

* Tue Aug 3 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-5
- fix shared lib warning, sort lib to devel
- choose GPLv2+ as License (until we know better)

* Wed Jul 28 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-4
- rename to lockfile
- sort lib to top package, fix license, build shared lib

* Sun Jul 18 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-3
- fix up hidden dirs, and links

* Wed Jun 30 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-2
- replace patch by sed-script

* Sat May 22 2010 Matthias Runge <mrunge@matthias-runge.de> 1.08-1
- initial build
