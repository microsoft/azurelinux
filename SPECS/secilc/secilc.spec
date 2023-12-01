%global libsepolver %{version}-1
Summary:        The SELinux CIL Compiler
Name:           secilc
Version:        3.2
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/%{name}-%{version}.tar.gz
Patch0:         Allow-setting-arguments-to-xmlto-via-environmental-var.patch
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  libsepol-devel >= %{libsepolver}
BuildRequires:  xmlto

%description
The SELinux CIL Compiler is a compiler that converts the CIL language as
described on the CIL design wiki into a kernel binary policy file.
Please see the CIL Design Wiki at:
http://github.com/SELinuxProject/cil/wiki/
for more information about the goals and features on the CIL language.

%prep
%autosetup -p1

%build
%{set_build_flags}
# xmlto wants to access a network resource for validation, so skip it
%make_build LIBSEPOL_STATIC=%{_libdir}/libsepol.a XMLARGS="--skip-validation" CFLAGS="%{build_cflags} -fno-semantic-interposition"

%install
%make_install SBINDIR="%{buildroot}%{_sbindir}" LIBDIR="%{buildroot}%{_libdir}"

%files
%license COPYING
%{_bindir}/secilc
%{_bindir}/secil2conf
%{_mandir}/man8/secilc.8.gz
%{_mandir}/man8/secil2conf.8.gz

%changelog
* Fri Aug 13 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream version and rebase patch
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream
- Update source URL to new format
- Lint spec
- License verified

* Fri Oct 09 2020 Olivia Crain <oliviacrain@microsoft.com> - 2.9-4
- Add missing %libsepolver definition

* Thu Aug 27 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-3
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- License verified

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 19 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Mon Mar 11 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc2.1
- SELinux userspace 2.9-rc2 release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc1.1
- SELinux userspace 2.9-rc1 release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri May 25 2018 Petr Lautrbach <plautrba@workstation> - 2.8-1
- SELinux userspace 2.8 release

* Tue May 15 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc3.1
- SELinux userspace 2.8-rc3 release candidate

* Mon Apr 23 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc1.1
- SELinux userspace 2.8-rc1 release candidate

* Tue Mar 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-5
- build: follow standard semantics for DESTDIR and PREFIX
- Describe multiple-decls in secilc.8.xml

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-3
- Rebuild with libsepol-2.7-3

* Fri Oct 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-2
- Fixed bad reference in roleattribute
- cil: Add ability to redeclare types[attributes]

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-1
- Update to upstream release 2017-08-04

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 15 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-1
- Update to upstream release 2016-10-14

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 04 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-6
- Rebuilt with libsepol-2.5-10

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-5
- Rebuilt with libsepol-2.5-9

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Rebuilt with libsepol-2.5-7

* Wed May 11 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- Rebuilt with libsepol-2.5-6

* Fri Apr 08 2016  - 2.5-2
- Add documentation and test rule for portcon dccp protocol

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Sun Feb 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-0.1.rc1
- Update to upstream rc1 release 2016-01-07

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Sep 01 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.4-6
- tell make where libsepol.a is to fix FTBFS on non-x86 64-bit archs - rhbz#1249522

* Wed Jul 29 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-5
- secilc-doc do not need the base package
- Fedora package review https://bugzilla.redhat.com/show_bug.cgi?id=1245270

* Thu Jul 23 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-4
- add license file

* Wed Jul 22 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-3
- remove unnecessary dependencies
- don't build libsepol

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-2
- make secilc-doc package noarch

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-1
- initial build based on libsepol-2.4 sources
