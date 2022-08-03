Name:           nfs4-acl-tools
Version:        0.3.7
Release:        1%{?dist}
Summary:        The nfs4 ACL tools
License:        BSD and GPLv2 and LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://git.linux-nfs.org/?p=bfields/nfs4-acl-tools.git;a=summary
Source0:        https://linux-nfs.org/~bfields/nfs4-acl-tools/%{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: libattr-devel

%description
This package contains commandline ACL utilities for the Linux
NFSv4 client.

%prep
%setup -q

%build
# Fix for autoconf 2.7.0+ build issues with missing config.guess and config.sub.
autoreconf --install
touch config.{guess,sub}

%configure \
    CC=gcc \
    CFLAGS="%{build_cflags} -D_FILE_OFFSET_BITS=64" \
    LDFLAGS="%{build_ldflags}"

%make_build

%install
%make_install

%files
%license COPYING
%doc INSTALL README TODO VERSION
%{_bindir}/nfs4_editfacl
%{_bindir}/nfs4_getfacl
%{_bindir}/nfs4_setfacl
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Mar 16 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.7-1
- Updating to 0.3.7.
- Fixing build issues with 'autoconf' 2.7.0+ by adding "CC=gcc" and running "autoreconf --install".
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.5-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.5-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct  6 2018 Steve Dickson <steved@redhat.com> - 0.3.5-0
- Updated to the latest upstream release: 0.3.5

* Sat Aug  4 2018 Steve Dickson <steved@redhat.com> - 0.3.4-0
- Updated to latest upstream release: 0.3.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 0.3.3-18
- use %%qmake_qt4 macro to ensure proper build flags

* Fri Jul 31 2015 Steve Dickson <steved@redhat.com> 0.3.3-17
- Handle the setting of DENY ace for DELETE, WRITE_OWNER (bz 1249103)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.3.3-15
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 15 2014 Nahum Shalman <nshalman-rpm@elys.com> 0.3.3-13
- Add patch to allow GUI tool to build correctly
- Package GUI tool in a child package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 16 2009 Steve Dickson <steved@redhat.com> - 0.3.3-6
- Fix a memory leak in nfs4_getfacl

* Mon Nov 16 2009 Steve Dickson <steved@redhat.com> - 0.3.3-5
- Fixes segfaulting issues with ACEs that have empty mask fields

* Thu Jul 30 2009 Steve Dickson <steved@redhat.com> - 0.3.3-4
- Change Group in spec file (bz 512580)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Steve Dickson <steved@redhat.com> - 0.3.3-1
- Updated to latest upstream version: 0.3.3

* Wed Oct 29 2008 Steve Dickson <steved@redhat.com> - 0.3.2-3
- Removed fuzzness from the compile.patch (bz 321745)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.2-2
- Autorebuild for GCC 4.3

* Fri Oct 26 2007 Steve Dickson <steved@redhat.com> - 0.3.2-1
- Updated to latest upstream version 0.3.2

* Tue Mar 27 2007 Steve Dickson <steved@redhat.com> - 0.3.1-1.2
- Checked in to Fedora CVS 

* Thu Mar  8 2007  Steve Dickson <steved@redhat.com> - 0.3.1-1.1
- Updated to latest upstream version 0.3.1 which eliminated the 
  need for the patches introduced in the previous commit.

* Tue Mar  6 2007  Tom "spot" Callaway <tcallawa@redhat.com> 0.3.0-1.1
- lose the BR for autotools
- Patch in support for destdir
- use %%configure macro, make DESTDIR= install
- add sparc to -fPIE (trivial, but correct)
- destdir revealed missing/poorly created symlink, patch fixes it, add nfs4_editfacl to files
- LDFLAGS passed to configure/exported were being blindly overwritten, patch fixes

* Fri Mar  2 2007  Steve Dickson <steved@redhat.com> - 0.3.0-1
- Updated to latest upstream version 0.3.0
- Fixed minor issues in spec file from the package review

* Fri Feb 16 2007 Steve Dickson <steved@redhat.com> - 0.2.0-1
- Initial commit
