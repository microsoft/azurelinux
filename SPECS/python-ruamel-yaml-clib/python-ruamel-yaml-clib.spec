%global pname ruamel-yaml-clib
%global commit 5f8ccce2f70b3a5d27c47ce19fe33e5bdd815571
Summary:        C version of reader, parser and emitter for ruamel.yaml derived from libyaml
Name:           python-%{pname}
Version:        0.2.8
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pypi.org/project/ruamel.yaml.clib/
Source0:        https://sourceforge.net/code-snapshots/hg/r/ru/ruamel-yaml-clib/code/ruamel-yaml-clib-code-%{commit}.zip
# ruamel has vendored a copy of libyaml but forgot to include libyaml's LICENSE file.
Source1:        LICENSE-libyaml
BuildRequires:  gcc

%description
It is the C based reader/scanner and emitter for ruamel.yaml.

%package -n     python3-%{pname}
Summary:        %{summary}
BuildRequires:  python3-Cython
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
Requires:       python3-ruamel-yaml

%description -n python3-%{pname}
It is the C based reader/scanner and emitter for ruamel.yaml.

%prep
%autosetup -n ruamel-yaml-clib-code-%{commit}
cp -p '%{SOURCE1}' .

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files _ruamel_yaml

%files -n python3-%{pname} -f %{pyproject_files}
%license LICENSE LICENSE-libyaml
%doc README.rst

%changelog
* Wed Feb 21 2024 Chris Gunn <chrisgun@mircosoft.com> - 0.2.8-1
- Update to 0.2.8
- Switch to sourceforge sources

* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.2.0-1
- Auto-upgrade to 0.2.0 - Azure Linux 3.0 - package upgrades

* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 0.1.2-7
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 12 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-5
- Force regenerating C files from Cython sources
- Require python3-ruamel-yaml

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Chandan Kumar <raukadah@gmail.com> - 0.1.2-1
- Initial package
