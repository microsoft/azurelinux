# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           liblockfile
Version:        1.17
Release: 12%{?dist}
Summary:        This implements a number of functions found in -lmail on SysV systems

# regarding license please see file COPYRIGHT
License:        GPL-2.0-or-later AND LGPL-2.0-or-later
URL:            http://packages.qa.debian.org/libl/liblockfile.html
Source0:        http://deb.debian.org/debian/pool/main/libl/liblockfile/liblockfile_%{version}.orig.tar.gz

BuildRequires:  gcc
BuildRequires: make

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
%setup -q -n %{name}-%{VERSION}

# There are occurrences of "install -g GROUP ...".
#
# Changing the group requires permissions that are normally not
# available while packaging.
#
# Let's remove "-g GROUP".
sed -Ei "/install/ s/-g [^ ]+//" Makefile.in

# Makefile.in mixes and messes with DESTDIR and prefix.
# See the following pull requests submitted upstream:
# https://github.com/miquels/liblockfile/pull/11
# https://github.com/miquels/liblockfile/pull/15
sed -i \
    -e '/^prefix/s,\$(DESTDIR),,' \
    -e 's,\(\$(\(lib\|include\|man\|nfslock\|bin\)dir)\),$(DESTDIR)\1,' \
    -e '/-DLOCKPROG/s,\$(DESTDIR),,' Makefile.in

%build
%configure --enable-shared --with-mailgroup
%make_build

%install
%make_install

ldconfig -N -n %{buildroot}/%{_libdir}

%ldconfig_scriptlets

%files
%attr(2755,root,mail) %{_bindir}/dotlockfile
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
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 16 2023 Richard Lescak <rlescak@redhat.com> - 1.17-5
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 17 2022 Fabrice Bauzac-Stehly <noon@mykolab.com> - 1.17-2
- Enable --with-mailgroup (rhbz#2040522)

* Fri Jan 28 2022 Richard Lescak <rlescak@redhat.com> - 1.17-1
- Rebase to version 1.17 

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
