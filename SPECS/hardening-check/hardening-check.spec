%global debug_package %{nil}

Summary:        Tool to check ELF binary hardening configuration
Name:           hardening-check
Version:        2.6
Release:        2%{?dist}
License:        GPLv2+
URL:            https://packages.debian.org/hardening-wrapper
Group:          Development/Tools
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
BuildArch:      noarch

Source0:        https://ftp.debian.org/debian/pool/main/h/hardening-wrapper/hardening-wrapper_%{version}.tar.xz

Requires:	binutils

%description
hardening-check is a tool to check whether an already compiled ELF file
was built using hardening flags.

It checks, using readelf, for these hardening characteristics:

  * Position Independent Executable
  * Stack protected
  * Fortify source functions
  * Read-only relocations
  * Immediate binding


%prep
%setup -n hardening-wrapper

# Remove debian-specific checks from Makefile.
%{__sed} -i.debian -e '/^[ \t]*if \[ -z \"\$.DEB_/d' Makefile

%build
make

%install
%{__install} -Dpm 0755 build-tree/hardening-check	\
	%{buildroot}%{_bindir}/hardening-check
%{__install} -Dpm 0644 build-tree/hardening-check.1	\
	%{buildroot}%{_mandir}/man1/hardening-check.1

%files
%doc TODO
%doc debian/README.Debian
%doc debian/changelog
%license AUTHORS
%license debian/copyright
%{_bindir}/hardening-check
%{_mandir}/man1/hardening-check.1.*

%changelog
* Wed May 20 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.6-2
- Initial CBL-Mariner import from Fedora 26 (license: MIT).
- Changed package name from 'hardening-wrapper'.

* Fri Jun 16 2017 Björn Esser <besser82@fedoraproject.org> - 2.6-1
- New upstream release (rhbz#1132836)

* Fri Jun 16 2017 Björn Esser <besser82@fedoraproject.org> - 2.5-6
- Fix upstream url (rhbz#1398730)
- Rename main-package to hardening-wrapper (rhbz#1444428)
- Run build archful, but build a noarch'ed binary-package
- Adapt spec-file to new guidelines

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Björn Esser <bjoern.esser@gmail.com> - 2.5-1
- new upstream release (#1044406)

* Thu Sep 19 2013 Björn Esser <bjoern.esser@gmail.com> - 2.4-1
- new upstream release (#1008372)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.3-3
- Perl 5.18 rebuild

* Sun Jun 09 2013 Björn Esser <bjoern.esser@gmail.com> - 2.3-2
- removed BuildRequires: binutils glibc-common
- not renaming docs in debian/
- removed terms to be possibly subject to bitrot from %%description
- as suggested by Ville Skyttä during review

* Fri Jun 07 2013 Björn Esser <bjoern.esser@gmail.com> - 2.3-1
- Initial rpm release (#971836)
