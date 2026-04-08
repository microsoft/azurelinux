# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global forgeurl https://github.com/RedHatOfficial/ksc
%global commitdate 20210216
%global commit 5955c6b2288353c5b093677221cc91a83a2c800c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%{?python_enable_dependency_generator}
%forgemeta

Name:		ksc
Version:	1.7
Release:	13%{?dist}
Summary:	Kernel source code checker
Group:		Development/Tools
AutoReqProv:	no
License:	GPL-2.0-or-later
URL:		https://github.com/RedHatOfficial/ksc
BuildArch:	noarch
Requires:	kmod
Requires:	binutils
Requires:	kernel-devel
Requires:	python3-requests
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
Source0:	https://github.com/RedHatOfficial/ksc/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

%description
A kernel module source code checker to find usage of select symbols

%prep
%forgesetup
# Fix build with setuptools 62.1
# https://github.com/RedHatOfficial/ksc/issues/3
sed -i "15i packages=[]," setup.py

%build
%py3_build

%install
%py3_install
install -D ksc.1 %{buildroot}%{_mandir}/man1/ksc.1

%files
%license COPYING
%doc README PKG-INFO
%{_bindir}/ksc
%{_datadir}/ksc
%{_mandir}/man1/ksc.*
%config(noreplace) %{_sysconfdir}/ksc.conf
%{python3_sitelib}/ksc-%{version}*.egg-info

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jun 19 2023 Čestmír Kalina <ckalina@redhat.com> - 1.7-8
- Migrate license to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Lumír Balhar <lbalhar@redhat.com> - 1.7-5
- Fix compatibility with newer setuptools

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Zamir SUN <sztsian@gmail.com> - 1.7-2
- Add python3-requests into Requires

* Tue Jan 05 2021 Čestmír Kalina <ckalina@redhat.com> - 1.7-1
- Initial Fedora commit.
