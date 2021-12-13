Vendor:         Microsoft Corporation
Distribution:   Mariner
%global libdnf_version 0.43.1

Name:           microdnf
Version:        3.5.1
Release:        2%{?dist}
Summary:        Minimal C implementation of DNF

License:        GPLv3+
URL:            https://github.com/rpm-software-management/microdnf
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  meson >= 0.36.0
BuildRequires:  pkgconfig(glib-2.0) >= 2.44.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.44.0
BuildRequires:  pkgconfig(libpeas-1.0) >= 1.20.0
BuildRequires:  pkgconfig(libdnf) >= %{libdnf_version}
BuildRequires:  pkgconfig(smartcols)
BuildRequires:  help2man

Requires:       libdnf%{?_isa} >= %{libdnf_version}

%description
Micro DNF is a very minimal C implementation of DNF's install, upgrade,
remove, repolist, and clean commands, designed to be used for doing simple
packaging actions in containers when you don't need full-blown DNF and
you want the tiniest useful containers possible.

That is, you don't want any interpreter stack and you want the most
minimal environment possible so you can build up to exactly what you need.

This is not a substitute for DNF for real systems, and many of DNF's
capabilities are intentionally not implemented in Micro DNF.


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
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.5.1-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Nov 26 2020 Nicola Sella <nsella@redhat.com> - 3.5.1-1
- Update to 3.5.1
- Relicense to GPLv2+
- Bump minimum version of libdnf in CMake and Meson
- Add module enable and disable commands
- Add reports of module changes
- Add "module enable" command
- Add subcommands support
- Print info about obsoleted packages before transaction (RhBug:1855542)

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
