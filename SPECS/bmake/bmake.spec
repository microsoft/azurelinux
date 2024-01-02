Summary:       The NetBSD make(1) tool
Name:          bmake
Version:       20230723
Release:       1%{?dist}
License:       BSD
Vendor:        Microsoft Corporation
Distribution:  Mariner
URL:           https://ftp.netbsd.org/pub/NetBSD/misc/sjg/
Source0:       %{url}/bmake-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: sed
BuildRequires: util-linux
Requires:      mk-files

%description
bmake, the NetBSD make tool, is a program designed to simplify the
maintenance of other programs.  The input of bmake is a list of specifications
indicating the files upon which the targets (programs and other files) depend.
bmake then detects which targets are out of date based on their dependencies
and triggers the necessary commands to bring them up to date when that happens.

bmake is similar to GNU make, even though the syntax for the advanced features
supported in Makefiles is very different.

%package -n mk-files
Summary:   Support files for bmake, the NetBSD make(1) tool
BuildArch: noarch

%description -n mk-files
The mk-files package provides some bmake macros derived from the NetBSD
bsd.*.mk macros.  These macros allow the creation of simple Makefiles to
build all kinds of targets, including, for example, C/C++ programs and/or
shared libraries.

%prep
%autosetup -p1 -n %{name}
sed -i.python -e '1 s|^#!/usr/bin/env python|#!/usr/bin/python3|' mk/meta2deps.py

%build
%configure --with-default-sys-path=%{_datadir}/mk
sh ./make-bootstrap.sh

%install
./bmake -m mk install DESTDIR=%{buildroot} INSTALL='install -p' STRIP_FLAG=''
chmod a-x %{buildroot}%{_datadir}/mk/mkopt.sh

%files
%doc ChangeLog README
%license LICENSE
%{_bindir}/*
%{_mandir}/man1/*

%files -n mk-files
%license LICENSE
%doc mk/README
%{_datadir}/mk

%changelog
* Fri Dec 08 2023 Andrew Phelps <anphel@microsoft.com> - 20230723-1
- Upgrade to version 20230723

* Tue Mar 22 2022 Cameron Baird <cameronbaird@microsoft.com> - 20211221-2
- Add patch remove-inconsistent-time-tests.patch, which disables unreliably failing
- tests in varmod-localtime.mk

* Mon Jan 10 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 20211221-1
- Upgrade to 20211221

* Fri Apr 16 2021 Vincent Tam <vtam@microsoft.com> - 20201010-2
- Disable tests for tcsh / ksh
- License verified
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Tue Oct 20 2020 Petr Menšík <pemensik@redhat.com> - 20201010-1
- Update to 20201010 (#1876115)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200710-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200710-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Petr Menšík <pemensik@redhat.com> - 20200710-1
- Update to 20200710

* Thu Jul 09 2020 Petr Menšík <pemensik@redhat.com> - 20200704-1
- Update to 20200704 (#1852609)
- Include license (#1845892)

* Wed Jun 10 2020 Petr Menšík <pemensik@redhat.com> - 20200524-3
- Make mk-files mandatory again

* Wed Jun 10 2020 Petr Menšík <pemensik@redhat.com> - 20200524-2
- Create mk-files subpackage from bmake sources

* Mon May 25 2020 Petr Menšík <pemensik@redhat.com> - 20200524-1
- Update to version 20200524

* Fri Feb 28 2020 Luis Bazan <lbazan@fedoraproject.org> - 20200212-1
- New upstream version

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20180512-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180512-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20180512-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180512-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May 29 2018 Luis Bazan <lbazan@fedoraproject.ort> - 20180512-1
- New Upstream version

* Wed Apr 25 2018 Luis Bazan <lbazan@fedoraproject.org> - 20180222-1
- New upstream version

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Luis Bazan <lbazan@fedoraproject.org> - 20171207-1
- New Upstream version

* Wed Nov 22 2017 Luis Bazan <lbazan@fedoraproject.org> - 20171118-1
- new upstream version

* Sun Nov 05 2017 Michel Alexandre Salim <salimma@fedoraproject.org> - 20171028-1
- New upstream version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20150910-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20150910-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20150910-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20150910-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Oct 03 2015 Luis Bazan <lbazan@fedoraproject.org> - 20150910-1
- new upstream version

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20141111-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Dec 15 2014 Luis Bazan <lbazan@fedoraproject.org> - 20141111-1
- New upstream version

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140620-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 2 2014 Luis Bazan <lbazan@fedoraproject.org> - 20140620-1
- new upstream version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20140214-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Feb 18 2014 Luis Bazan <lbazan@fedoraproject.org> - 20140214-1
- new upstream version

* Wed Jan 15 2014 Luis Bazan <lbazan@fedoraproject.org> - 20140101-1
- New Upstream version

* Tue Oct 29 2013 Luis Bazan <lbazan@fedoraproject.org> - 20131001-1
- New Upstream version

* Wed Aug 14 2013 Luis Bazan <lbazan@fedoraproject.org> - 20130730-1
- New Upstream Version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20130330-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 16 2013 Luis Bazan <lbazan@fedoraproject.org> - 20130330-1
- New Upstream Version

* Wed Mar 06 2013 Luis Bazan <lbazan@fedoraproject.org> - 20130123-1
- New Upstream Version

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120831-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Sep 05 2012 Luis Bazan <lbazan@fedoraproject.org> - 20120831-1
- New Upstream Version

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20120604-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Luis Bazan <bazanluis20@gmail.com> 20120604-2
- Changing destination of the sources

* Tue Jun 05 2012 Luis Bazan <bazanluis20@gmail.com> 20120604-1
- New Upstream Version 20120604-1.

* Mon Feb 06 2012 Julio Merino <jmmv@NetBSD.org> 20111111-1
- New upstream version.

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090222-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090222-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20090222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Stepan Kasal <skasal@redhat.com> - 20090222-1
- new upstream version

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080515-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 02 2008 Julio M. Merino Vidal <jmmv@NetBSD.org> - 20080515-1
- Initial release for Fedora.
