%global libdnf_version 0.62.0

Distribution:   Azure Linux
Vendor:         Microsoft Corporation

Name:           microdnf
Version:        3.10.1
Release:        2%{?dist}
Summary:        Lightweight implementation of DNF in C

License:        GPL-2.0-or-later
URL:            https://github.com/rpm-software-management/microdnf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.36.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.44.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.44.0
BuildRequires:  pkgconfig(libpeas-1.0) >= 1.20.0
BuildRequires:  pkgconfig(libdnf) >= %{libdnf_version}
BuildRequires:  pkgconfig(smartcols)
BuildRequires:  help2man

Requires:       libdnf%{?_isa} >= %{libdnf_version}
# Ensure DNF package manager configuration skeleton is installed
Requires:       /etc/dnf/dnf.conf

%description
Micro DNF is a lightweight C implementation of DNF, designed to be used
for doing simple packaging actions when you don't need full-blown DNF and
you want the tiniest useful environments possible.

That is, you don't want any interpreter stack and you want the most
minimal environment possible so you can build up to exactly what you need.


%prep
%autosetup -p1

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc README.md
%{_mandir}/man8/microdnf.8*
%{_bindir}/%{name}

%changelog
* Tue Jan 28 2025 Archana Shettigar <v-shettigara@microsoft.com> - 3.10.1-2
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License Verified

* Wed Dec 11 2024 Evan Goode <egoode@redhat.com> - 3.10.1-1
- Update to 3.10.1
- Correct spelling of summary
- Print more helpful error message when reinstalling non-installed pkg

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Jan Kolarik <jkolarik@redhat.com> - 3.10.0-2
- Don't use libdnf5 as a dependency

* Tue Jun 06 2023 Jan Kolarik <jkolarik@redhat.com> - 3.10.0-1
- Update to 3.10.0
- Add swap command
- Prepare for dnf5 transition in Fedora 39

* Fri May 19 2023 Petr Pisar <ppisar@redhat.com> - 3.9.0-3
- Rebuild against rpm-4.19 (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Aug 15 2022 Jaroslav Rohel <jrohel@redhat.com> - 3.9.0-1
- Update to 3.9.0
- Add leaves command - List installed packages not required by other installed packages

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Mar 14 2022 Pavla Kratochvilova <pkratoch@redhat.com> - 3.8.1-1
- Remove non-breaking space from "Size" column (RhBug:2010676)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 19 2021 Nicola Sella <nsella@redhat.com> - 3.8.0-1
- Update to 3.8.0
- distrosync: Fix style issues and plugin build with Meson 
- Add distro-sync subcommand
- Add "makecache" command 

* Tue Mar 02 2021 Nicola Sella <nsella@redhat.com> - 3.7.1-1
- Update to 3.7.1
- [download] fix: unwanted dependency on newer glib 
- [download] Support for "--resolve" and "--alldeps" arguments 
- [download] New get_packages_query function
- Support "--setopt=keepcache=0/1"
- [download] Support "--archlist=" argument
- [download] Move package download code to "download_packages" function
- [download] several optimizations
- Don't set default value of "assumeyes" to TRUE 
- Support for user confirmation and assumeyes, assumeno, defaultyes
- Extend "--setopt" to support repository options 
- Added alias "update" to "upgrade" command
- Command "update" renamed to "upgrade"
- Add support for command aliases
- dnf-data requirement only for Fedora and future RHEL
- Relicense to GPLv2+ [errata corrige: not in 3.5.1-1]
- Sync summary and description from openSUSE [errata corrige: not in 3.6.0-1]

* Thu Jan 28 2021 Nicola Sella <nsella@redhat.com> - 3.6.0-1
- Update to 3.6.0
- spec: Sync summary and description from openSUSE
- Add support for setting a platform module ID
- Add dependency for DNF configurations skeleton
- Add support for setting allow_vendor_change

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 26 2020 Nicola Sella <nsella@redhat.com> - 3.5.1-1
- Update to 3.5.1
- Relicense to GPLv2+
- Bump minimum version of libdnf in CMake and Meson

* Fri Nov 13 2020 Nicola Sella <nsella@redhat.com> - 3.5.0-1
- Update to 3.5.0
- Add module enable and disable commands
- Add reports of module changes
- Add "module enable" command
- Add subcommands support
- Print info about obsoleted packages before transaction (RhBug:1855542)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Ales Matej <amatej@redhat.com> - 3.4.0-1
- Add reinstall command
- Add "--setopt=tsflags=test" support
- Add "--setopt=reposdir=<path>" and "--setopt=varsdir=<path1>,<path2>,..." support
- Add "--config=<path_to_config_file>" support
- Add "--disableplugin", "--enableplugin" support (RhBug:1781126)
- Add "--noplugins" support
- Add "--setopt=cachedir=<path_to_cache_directory>" support
- Add "--installroot=<path_to_installroot_directory>" support
- Add "--refresh" support
- Support "install_weak_deps" conf option and "--setopt=install_weak_deps=0/1"
- Respect reposdir from conf file
- Respect "metadata_expire" conf file opton (RhBug:1771147)
- Fix: Don't print lines with (null) in transaction report (RhBug:1691353)
- [repolist] Print padding spaces only if output is terminal

* Fri Nov 29 2019 Ales Matej <amatej@redhat.com> - 3.3.0-1
- Update to 3.3.0
- Fix: do not download metadata in remove command
- Add repolist command (RhBug:1584952) 
- Add repoquery command (RhBug:1769245) 

* Wed Nov 06 2019 Pavla Kratochvilova <pkratoch@redhat.com> - 3.0.2-1
- Update to 3.0.2
- Add support for --releasever (RhBug:1591627)
- Fix minor memory leaks (RhBug:1702283)
- Use help2man to generate a man page (RhBug:1612520)
- Allow downgrade for all transactions microdnf does (RhBug:1725863)
- Add options --best and --nobest for transactions (RhBug:1679476)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jaroslav Mracek <jmracek@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 22 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3-2
- No CMake, only meson

* Thu Jun 01 2017 Igor Gnatenko <ignatenko@redhat.com> - 3-1
- Update to 3

* Fri May 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 2-3
- Apply few patches from upstream

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 02 2017 Igor Gnatenko <ignatenko@redhat.com> - 2-1
- Update to 2

* Mon Dec 12 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1-1
- Initial package
