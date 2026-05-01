# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package serves both as a build backend and a tool for theme developers.
# During the Python bootstrap we need the build functionality for python-furo.
# cli extra, needed for the application usage, has got a long chain of
# dependencies leading ultimately to python-django which can be built much
# later in the bootstrap process, hence the bcond to build just the "core" parts.
%bcond bootstrap 0

%global prerel  b2
%global giturl  https://github.com/pradyunsg/sphinx-theme-builder

Name:           python-sphinx-theme-builder
Version:        0.2.0
Release:        0.25.%{prerel}%{?dist}
Summary:        Streamline the Sphinx theme development workflow

# Most of the code is MIT.  However,
# src/sphinx_theme_builder/_internal/passthrough.py is BSD-3-Clause.
License:        MIT AND BSD-3-Clause
URL:            https://sphinx-theme-builder.readthedocs.io/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}%{prerel}/sphinx-theme-builder-%{version}%{prerel}.tar.gz
# Compatibility fix for python 3.14
# https://github.com/pradyunsg/sphinx-theme-builder/pull/51
Patch:          0001-Avoid-ast.Str-for-python-3.14-compatibility.patch

BuildArch:      noarch

BuildRequires:  help2man
BuildRequires:  python3-devel

%description
A tool for authoring Sphinx themes with a simple (opinionated) workflow.

%package     -n python3-sphinx-theme-builder
Summary:        Streamline the Sphinx theme development workflow

%description -n python3-sphinx-theme-builder
A tool for authoring Sphinx themes with a simple (opinionated) workflow.

%if %{without bootstrap}
%pyproject_extras_subpkg -n python3-sphinx-theme-builder cli
%{_bindir}/stb
%{_mandir}/man1/stb.1*
%endif

%prep
%autosetup -n sphinx-theme-builder-%{version}%{prerel} -p1

%conf
# Use local objects.inv for intersphinx
sed -e 's|\("https://docs\.python\.org/3", \)None|\1"%{_docdir}/python3-docs/html/objects.inv"|' \
    -e 's|\("https://www\.sphinx-doc\.org/en/master", \)None|\1"%{_docdir}/python-sphinx-doc/html/objects.inv"|' \
    -i docs/conf.py

%generate_buildrequires
# Skip test packages not available in Fedora
sed -i '/pytest-clarity/d;/pytest-pspec/d' tests/requirements.txt
%pyproject_buildrequires %{!?with_bootstrap:-x cli tests/requirements.txt}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -L sphinx_theme_builder

%if %{without bootstrap}
# Install a man page
mkdir -p %{buildroot}%{_mandir}/man1
%{py3_test_envvars} help2man -N --version-string=%{version}%{prerel} \
  -n 'Streamline the Sphinx theme development workflow' \
  %{buildroot}%{_bindir}/stb > %{buildroot}%{_mandir}/man1/stb.1
%else
# without cli there's no use of the binary file
rm %{buildroot}%{_bindir}/stb
%endif

%check
%if %{without bootstrap}
%pytest -v
%else
%pyproject_check_import
%endif

%files -n python3-sphinx-theme-builder -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.0-0.25.b2
- Rebuilt for Python 3.14.0rc3 bytecode

* Thu Sep 04 2025 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-0.24.b2
- Remove patch for compatibility with click 8.2
- Due to numerous regressions, we are going to revert back to click 8.1.7

* Fri Aug 22 2025 Jerry James <loganjerry@gmail.com> - 0.2.0-0.23.b2
- Add patch for compatibility with click 8.2

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.0-0.22.b2
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.21.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 0.2.0-0.20.b2
- Bootstrap for Python 3.14.0b3 bytecode

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.2.0-0.19.b2
- Bootstrap for Python 3.14

* Mon Jan 27 2025 Jerry James <loganjerry@gmail.com> - 0.2.0-0.18.b2
- Python 3.14 compatibility fix (rhbz#2342318)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.17.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.16.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Jerry James <loganjerry@gmail.com> - 0.2.0-0.15.b2
- Build in non-bootstrap mode
- Minor spec file cleanups

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.2.0-0.15.b2
- Bootstrap for Python 3.13

* Fri Feb 16 2024 Karolina Surma <ksurma@redhat.com> - 0.2.0-0.14.b2
- Make cli extra optional to cut off the long dependency chain when
bootstrapping new Python

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.13.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.12.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.11.b2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.2.0-0.10.b2
- Rebuilt for Python 3.12

* Mon Apr 24 2023 Jerry James <loganjerry@gmail.com> - 0.2.0-0.9.b2
- Use %%py3_test_envvars to simplify man page installation

* Wed Apr 19 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.2.0-0.9.b2
- Unused docs BuildRequires were dropped to remove a dependency loop between
python-sphinx-theme-builder and python-furo

* Tue Mar 28 2023 Jerry James <loganjerry@gmail.com> - 0.2.0-0.8.b2
- Version 0.2.0b2
- Drop upstreamed tomllib patch

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 0.2.0-0.7.b1
- Add cli extras subpackage containing the stb binary
- Dynamically generate BuildRequires

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.6.b1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Jerry James <loganjerry@gmail.com> - 0.2.0-0.5.b1
- Drop dependency on tomli
- Convert License tag to SPDX

* Fri Jul 29 2022 Jerry James <loganjerry@gmail.com> - 0.2.0-0.4.b1
- Version 0.2.0b1
- Depend on pyproject-metadata instead of pep621

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.3.a15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Jerry James <loganjerry@gmail.com> - 0.2.0-0.2.a15
- Version 0.2.0a15

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 0.2.0-0.2.a14
- Rebuilt for Python 3.11

* Tue Apr 12 2022 Jerry James <loganjerry@gmail.com> - 0.2.0-0.1.a14
- Initial RPM
