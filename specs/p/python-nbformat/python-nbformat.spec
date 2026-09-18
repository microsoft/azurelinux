# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Unset -s on python shebang - ensure that extensions installed with pip
# to user locations are seen and properly loaded
%global py3_shebang_flags %(echo %py3_shebang_flags | sed s/s//)

%global srcname nbformat

Name:           python-%{srcname}
Version:        5.10.4
Release:        5%{?dist}
Summary:        The Jupyter Notebook format

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        https://files.pythonhosted.org/packages/source/n/%{srcname}/%{srcname}-%{version}.tar.gz
# Removed dependency on hatch-nodejs-version
Patch0:         nbformat-build-test.patch
# Remove dependency on pep440 (package will be retired)
Patch1:         https://github.com/jupyter/nbformat/pull/408.patch

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
# For tests
BuildRequires:  python%{python3_pkgversion}-fastjsonschema
BuildRequires:  python%{python3_pkgversion}-testpath

%description
This package contains the base implementation of the Jupyter Notebook format,
and Python APIs for working with notebooks.


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        The Jupyter Notebook format
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
This package contains the base implementation of the Jupyter Notebook format,
and Python APIs for working with notebooks.


%prep
%autosetup -p1 -n %{srcname}-%{version}
mkdir -p nbformat/tests

# Remove useless test dependencies
sed -i '/"pre-commit",/d' pyproject.toml
sed -i '/"check-manifest",/d' pyproject.toml

# Set version statically
# {VERSION} is a part of Patch0
sed -i "s/{VERSION}/%{version}/" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -r -x test

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
# Ignore failure for now
# https://github.com/jupyter/nbformat/issues/405
%pytest -p no:unraisableexception

 
%files -n python%{python3_pkgversion}-%{srcname} -f %pyproject_files
%doc CHANGELOG.md README.md
%license LICENSE
%{_bindir}/jupyter-trust

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.10.4-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.10.4-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 5.10.4-2
- Rebuilt for Python 3.14

* Sat Mar 15 2025 Orion Poplawski <orion@nwra.com> - 5.10.4-1
- Update to 5.10.4

* Sat Feb 08 2025 Sandro <devel@penguinpee.nl> - 5.9.2-8
- Drop dependency on pep440

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 5.9.2-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 5.9.2-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 07 2023 Orion Poplawski <orion@nwra.com> - 5.9.2-1
- Update to 5.9.2

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 16 2023 Orion Poplawski <orion@nwra.com> - 5.9.1-1
- Update to 5.9.1

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 5.8.0-2
- Rebuilt for Python 3.12

* Sun May 28 2023 Orion Poplawski <orion@nwra.com> - 5.8.0-1
- Update to 5.8.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Lumír Balhar <lbalhar@redhat.com> - 5.7.0-1
- Update to 5.7.0 (rhbz#1909560)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 5.4.0-2
- Rebuilt for Python 3.11

* Wed Jun 08 2022 Orion Poplawski <orion@nwra.com> - 5.4.0-1
- Update to 5.4.0

* Sat Jan 29 2022 Orion Poplawski <orion@nwra.com> - 5.1.3-1
- Update to 5.1.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Karolina Surma <ksurma@redhat.com> - 5.0.8-5
- Remove -s from Python shebang in `jupyter-trust` to let Jupyter see
  pip installed extensions

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.0.8-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 27 2020 Orion Poplawski <orion@nwra.com> - 5.0.8-1
- Update to 5.0.8

* Wed Sep 09 2020 Lumír Balhar <lbalhar@redhat.com> - 5.0.7-1
- Update to 5.0.7 (#1425643)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 5.0.5-2
- Rebuilt for Python 3.9

* Fri May 08 2020 Orion Poplawski <orion@nwra.com> - 5.0.5-1
- Update to 5.0.5

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 23 2020 Orion Poplawski <orion@nwra.com> - 5.0.4-1
- Update to 5.0.4

* Sun Jan 12 2020 Orion Poplawski <orion@nwra.com> - 5.0.3-1
- Update to 5.0.3 (bz#1789213)

* Thu Sep 26 2019 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-9
- Correct the BR of python3-jupyter-core

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-6
- Subpackage python2-nbformat has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Aug 29 2017 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-1
- Update to 4.4.0

* Tue Aug  8 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.3.0-3
- Fix %%python_provide invocation

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Orion Poplawski <orion@cora.nwra.com> - 4.3.0-1
- Update to 4.3.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-2
- Rebuild for Python 3.6

* Sat Dec 17 2016 Orion Poplawski <orion@cora.nwra.com> - 4.2.0-1
- Update to 4.2.0
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Wed Jul 15 2015 Orion Poplawski <orion@cora.nwra.com> - 4.0.0-2
- Fixup BRs and EL7 build

* Mon Jul 13 2015 Orion Poplawski <orion@cora.nwra.com> - 4.0.0-1
- Initial package
