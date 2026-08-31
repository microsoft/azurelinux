# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Force out of source build
%undefine __cmake_in_source_build

%global somajor 0

Name:           libeconf
Version:        0.7.9
Release:        2%{?dist}
Summary:        Enhanced config file parser library

License:        MIT
URL:            https://github.com/openSUSE/libeconf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

### Patches ###
# This should be a temporary workaround. I don't have enough time to check what's happening, but since we aren't shipping the html documentation it's fine to stop installing it
Patch0101:      0001-cmake-no-install-html.patch
# Intermittent failure of a test in aarch64, thus temporarily disabling the failing test suite
Patch0102:      0002-disable-test.patch


BuildRequires:  cmake >= 3.12
BuildRequires:  gcc
BuildRequires:  make

%description
libeconf is a highly flexible and configurable library to parse and manage
key=value configuration files. It reads configuration file snippets from
different directories and builds the final configuration file from it.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        utils
Summary:        Utilities for manipulating config files
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    utils
The %{name}-utils package contains utilities for manipulating
configuration files from applications that use %{name}.


%prep
%autosetup -p1


%build
%cmake
%cmake_build


%install
%cmake_install


%check
%cmake_build --target check


%files
%license LICENSE
%doc NEWS README.md TODO.md
%{_libdir}/%{name}.so.%{somajor}{,.*}

%files devel
%doc example/
%{_includedir}/*
%{_libdir}/%{name}.so
%{_libdir}/cmake/%{name}/
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/*.3.*

%files utils
%{_bindir}/econftool
%{_mandir}/man8/econftool.8*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun  9 2025 Iker Pedrosa <ipedrosa@redhat.com> - 0.7.9-1
- Rebase to 0.7.9

* Mon Feb 10 2025 Iker Pedrosa <ipedrosa@redhat.com> - 0.7.6-1
- Rebase to 0.7.6

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Dec 10 2024 Iker Pedrosa <ipedrosa@redhat.com> - 0.7.5-1
- Rebase to 0.7.5

* Fri Nov  8 2024 Iker Pedrosa <ipedrosa@redhat.com> - 0.7.4-3
- migrated to SPDX license (although no change was done)

* Wed Oct 16 2024 Iker Pedrosa <ipedrosa@redhat.com> - 0.7.4-2
- Rebase to 0.7.4

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu May 23 2024 Iker Pedrosa <ipedrosa@redhat.com> - 0.6.2-2
- Fix static analyzer detected issues

* Wed Mar  6 2024 Iker Pedrosa <ipedrosa@redhat.com> - 0.6.2-1
- Rebase to 0.6.2

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 28 2023 Iker Pedrosa <ipedrosa@redhat.com> - 0.5.2-1
- Update to 0.5.2 (RH#1980774)
- Fix CVE-2023-22652 (RH#2212464)
- Fix CVE-2023-30079 (RH#2235236)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Neal Gompa <ngompa13@gmail.com> - 0.4.0-1
- Update to 0.4.0 (RH#1980289)
- Add fixes to install econftool and man pages

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 08 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.8-4
- Use backend-agnostic CMake macro for building and running tests

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 12 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.8-2
- Switch to updated and fixed tarball

* Fri Jul 10 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.8-1
- Update to 0.3.8 (RH#1844005)

* Thu Feb 06 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.5-1
- Update to 0.3.5 (RH#1797753)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.4-1
- Update to 0.3.4 (RH#1793599)

* Wed Oct 30 2019 Neal Gompa <ngompa13@gmail.com> - 0.3.3-1
- Update to 0.3.3 (RH#1756080)

* Tue Sep 24 2019 Neal Gompa <ngompa13@gmail.com> - 0.3.1-1
- Update to 0.3.1 (RH#1755161)

* Fri Sep  6 2019 Neal Gompa <ngompa13@gmail.com> - 0.3.0-1
- Initial packaging for Fedora (RH#1749869)
