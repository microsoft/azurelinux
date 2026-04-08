# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-notebook-shim
Version:        0.2.4
Release:        8%{?dist}
Summary:        A shim layer for notebook traits and config
License:        BSD-3-Clause
URL:            https://pypi.org/project/notebook-shim/
Source:         %{pypi_source notebook_shim}

BuildArch:      noarch
BuildRequires:  python3-devel
# https://github.com/jupyter/notebook_shim/issues/28
BuildRequires:  python3-pytest-jupyter

%global _description %{expand:
This project provides a way for JupyterLab and other frontends
to switch to Jupyter Server for their Python Web application backend.}


%description %_description

%package -n     python3-notebook-shim
Summary:        %{summary}

Requires:  python-jupyter-filesystem

%description -n python3-notebook-shim %_description


%prep
%autosetup -p1 -n notebook_shim-%{version}

# pytest-tornasync will never be available in Fedora
# and upstream will switch to pytest-jupyter soon
sed -i "/pytest-tornasync/d" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files notebook_shim

install -m 0755 -p -d %{buildroot}%{_sysconfdir}/jupyter/jupyter_server_config.d
mv -v %{buildroot}{%{_prefix},}%{_sysconfdir}/jupyter/jupyter_server_config.d/notebook_shim.json


%check
%pytest


%files -n python3-notebook-shim -f %{pyproject_files}
%doc README.md
%config(noreplace) %{_sysconfdir}/jupyter/jupyter_server_config.d/notebook_shim.json


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.4-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.4-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 05 2025 Python Maint <python-maint@redhat.com> - 0.2.4-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 0.2.4-2
- Rebuilt for Python 3.13

* Thu Feb 15 2024 Lumír Balhar <lbalhar@redhat.com> - 0.2.4-1
- Update to 0.2.4 (rhbz#2264315)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 0.2.3-2
- Rebuilt for Python 3.12

* Tue Apr 25 2023 Lumír Balhar <lbalhar@redhat.com> - 0.2.3-1
- Update to 0.2.3 (rhbz#2189303)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Lumír Balhar <lbalhar@redhat.com> - 0.2.2-1
- Initial package
