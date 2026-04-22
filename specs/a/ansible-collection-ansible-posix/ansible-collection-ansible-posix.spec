# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if %{undefined rhel}
%bcond_without tests
%else
%bcond_with tests
%endif

Name:           ansible-collection-ansible-posix
Version:        2.1.0
Release: 2%{?dist}
Summary:        Ansible Collection targeting POSIX and POSIX-ish platforms

# plugins/module_utils/mount.py: Python Software Foundation License version 2
License:        GPL-3.0-or-later AND PSF-2.0
URL:            %{ansible_collection_url ansible posix}
Source:         https://github.com/ansible-collections/ansible.posix/archive/%{version}/%{name}-%{version}.tar.gz
# Exclude unneceesary development files and duplicate docs from the built
# collection. This is a downstream only patch. Upstreams include these files
# for reasons that are irrelevant to Fedora.
Patch0:         0001-Exclude-unnecessary-files-from-built-collection.patch
BuildRequires:  ansible-packaging
%if %{with tests}
BuildRequires:  ansible-packaging-tests
%endif

BuildArch:      noarch


%description
%{summary}.


%prep
%autosetup -n ansible.posix-%{version} -p1
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +


%build
%ansible_collection_build


%install
%ansible_collection_install


%check
%if %{with tests}
%ansible_test_unit
%endif


%files -f %{ansible_collection_filelist}
%license COPYING PSF-license.txt
%doc README.md CHANGELOG.rst


%changelog
* Fri Dec 05 2025 Maxwell G <maxwell@gtmx.me> - 2.1.0-1
- Update to 2.1.0. Fixes rhbz#2381567.

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Maxwell G <maxwell@gtmx.me> - 2.0.0-1
- Update to 2.0.0. Fixes rhbz#2312056.

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 19 2023 Maxwell G <maxwell@gtmx.me> - 1.5.4-1
- Update to 1.5.4. Fixes rhbz#2207695.

* Fri Apr 14 2023 Maxwell G <maxwell@gtmx.me> - 1.5.2-1
- Update to 1.5.2. Fixes rhbz#2185694.

* Tue Jan 24 2023 Maxwell G <gotmax@e.email> - 1.5.1-1
- Update to 1.5.1. Fixes rhbz#2162988.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 24 2022 Maxwell G <gotmax@e.email> - 1.4.0-1
- Update to 1.4.0. Fixes rhbz#2089504.

* Tue May 10 2022 Maxwell G <gotmax@e.email> - 1.3.0-5
- Rebuild for new ansible-packaging.

* Tue Feb 22 2022 Maxwell G <gotmax@e.email> - 1.3.0-4
- Switch to ansible-packaging.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

Thu Oct 14 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.3.0-2
- Use ansible or ansible-core as BuildRequires

* Mon Sep 06 2021 Kevin Fenzi <kevin@scrye.com> - 1.3.0-1
- Update to 1.3.0. Fixes rhbz#1992970

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 24 2021 Kevin Fenzi <kevin@scrye.com> - 1.2.0-1
- Update to 1.2.0.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 1.1.1-2
- Rebuild against new ansible-generator and allow to be used by ansible-base-2.10.x

* Tue Dec 29 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 1.1.0-1
- Initial package
