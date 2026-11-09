# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           ansible-collection-containers-podman
Version:        1.16.3
Release: 9%{?dist}
Summary:        Podman Ansible collection for Podman containers

License:        GPL-3.0-or-later
URL:            %{ansible_collection_url containers podman}
Source:         https://github.com/containers/ansible-podman-collections/archive/%{version}.tar.gz

BuildRequires:  ansible-packaging

BuildArch:      noarch

%description
%{summary}.

%prep
%autosetup -n ansible-podman-collections-%{version}
sed -i -e 's/version:.*/version: %{version}/' galaxy.yml
find -type f ! -executable -name '*.py' -print -exec sed -i -e '1{\@^#!.*@d}' '{}' +
rm -vr changelogs/ ci/ contrib/ tests/ ./galaxy.yml.in .github/ .gitignore docs/

%build
%ansible_collection_build

%install
%ansible_collection_install

%files -f %{ansible_collection_filelist}
%license COPYING
%doc README.md

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 30 2025 Sagi Shnaidman <sshnaidm@redhat.com> - 1.16.3-1
- Bump to 1.16.3

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 30 2024 Sagi Shnaidman <sshnaidm@redhat.com> - 1.12.0-1
- Bump to 1.12.0

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Maxwell G <gotmax@e.email> - 1.10.1-1
- Update to 1.10.1. Fixes rhbz#2143801.
- Remove useless docs directory from collection artifact.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild


* Mon Jul 04 2022 Jakob Meng <code@jakobmeng.de> - 1.9.4-1
- Bump to 1.9.4

* Wed Mar 30 2022 Jakob Meng <code@jakobmeng.de> - 1.9.3-1
- Bump to 1.9.3

* Mon Mar 21 2022 Jakob Meng <code@jakobmeng.de> - 1.9.2-1
- Bump to 1.9.2

* Sat Jan 29 2022 Maxwell G <gotmax@e.email> - 1.9.1-3
- Switch to ansible-packaging.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Sagi Shnaidman <sshnaidm@redhat.com> - 1.9.1-1
- Bump to 1.9.1

* Thu Nov 25 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.8.3-1
- Bump to 1.8.3

* Tue Nov 09 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.8.2-1
- Bump to 1.8.2

* Thu Oct 14 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.6.1-3
- Use ansible or ansible-core as BuildRequires

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.6.1-1
- Bump to 1.6.1-1

* Sun Feb 21 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.4.1-2
- Resolving RPM issues

* Tue Feb 09 2021 Sagi Shnaidman <sshnaidm@redhat.com> - 1.4.1-1
- Initial package
