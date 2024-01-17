%global build_flags prefix=%{_prefix} lib_dir=%{_libdir} libexec_dir=%{_libexecdir}/%{name} etc_dir=%{_sysconfdir}/%{name}

Name:           authbind
Version:        2.1.3
Release:        1%{?dist}
Summary:        Allow non-root users to open restricted ports
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.chiark.greenend.org.uk/ucgi/~ian/git/authbind.git/
Source0:        https://deb.debian.org/debian/pool/main/a/%{name}/%{name}_%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         authbind-makefile-fixes.patch

BuildRequires:  gcc
BuildRequires:  make

%description
This package allows a package to be started as non-root but still bind to low
ports, without any changes to the application.

%prep
%autosetup -n %{name} -p1

%build
%set_build_flags
%make_build %{build_flags} OPTIMISE="$CFLAGS" LDFLAGS="$LDFLAGS"

%install
%make_install %{build_flags} STRIP=%{_bindir}/true

%files
%license debian/copyright
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.1*
%{_libexecdir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/byaddr
%dir %{_sysconfdir}/%{name}/byport
%dir %{_sysconfdir}/%{name}/byuid

%changelog
* Mon Jan 08 2024 Archana Choudhary <archana1@microsoft.com> - 2.1.3-1
- Upgrade to version 2.1.3
- Repackage tarball to align with folder structure expected

* Fri Feb 17 2023 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.1.2-4
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- License Verified

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 2.1.2-1
- Initial import; Fixes: RHBZ#2058364
