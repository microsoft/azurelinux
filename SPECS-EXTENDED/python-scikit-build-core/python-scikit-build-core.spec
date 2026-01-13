Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global debug_package %{nil}

# On epel python hatch/trove classifier check may fail because of old package
# Fedora checks should be sufficient though.
%bcond no_classifier_check 0%{?rhel}

Name:           python-scikit-build-core
Version:        0.11.5
Release:        5%{?dist}
Summary:        Build backend for CMake based projects

# The main project is licensed under Apache-2.0, but it has a vendored project
# src/scikit_build_core/_vendor/pyproject_metadata: MIT
# https://github.com/scikit-build/scikit-build-core/issues/933
License:        Apache-2.0 AND MIT
URL:            https://github.com/scikit-build/scikit-build-core
Source:         %{pypi_source scikit_build_core}

BuildRequires:  python-pip
BuildRequires:  python-hatchling
BuildRequires:  python-hatch-vcs
BuildRequires:  python-tomli
BuildRequires:  python-pathspec
BuildRequires:  python-packaging
BuildRequires:  python-editables
BuildRequires:  python-pluggy
BuildRequires:  python-setuptools_scm
BuildRequires:  python-trove-classifiers
BuildRequires:  python3-pytest
BuildRequires:  python3-virtualenv
BuildRequires:  python3-numpy
BuildRequires:  python3-devel

# Testing dependences
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  git

%global _description %{expand:
A next generation Python CMake adapter and Python API for plugins
}

%description %_description

%package -n python3-scikit-build-core
Summary:        %{summary}
Requires:       cmake
Requires:       ninja-build
BuildArch:      noarch

Provides:       bundled(python3dist(pyproject-metadata)) = 0.9.1

Obsoletes:      python3-scikit-build-core+pyproject < 0.10.7-3

%description -n python3-scikit-build-core %_description


%prep
%autosetup -n scikit_build_core-%{version}
# Rename the bundled license so that it can be installed together
cp -p src/scikit_build_core/_vendor/pyproject_metadata/LICENSE LICENSE-pyproject-metadata

# Remove unsupported Python 3.14 classifier (keep valid ones like 3.12)
sed -i '/Programming Language :: Python :: 3\.14/d' pyproject.toml


%generate_buildrequires
%if %{with no_classifier_check}
export HATCH_METADATA_CLASSIFIERS_NO_VERIFY=1
%endif
%pyproject_buildrequires -x test,test-meta,test-numpy


%build
%if %{with no_classifier_check}
export HATCH_METADATA_CLASSIFIERS_NO_VERIFY=1
%endif
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files scikit_build_core

#skipping check section
%check
%pyproject_check_import scikit_build_core
true

%files -n python3-scikit-build-core -f %{pyproject_files}
%license %{python3_sitelib}/scikit_build_core-%{version}.dist-info/licenses/*
%doc README.md


%changelog
* Fri Nov 28 2025 BinduSri Adabala <v-badabala@microsoft.com> - 0.11.5-5
- Initial Azure Linux import from Fedora 43 (license: MIT).
- License verified

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.11.5-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.11.5-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 Packit <hello@packit.dev> - 0.11.5-1
- Update to 0.11.5 upstream release

* Wed May 21 2025 Miro Hrončok <miro@hroncok.cz> - 0.11.0-2
- Avoid cattrs test dependency to unblock the Python 3.14 rebuild

* Fri Feb 28 2025 Cristian Le <git@lecris.dev> - 0.11.0-1
- Update to 0.11.0 upstream release
- Resolves: rhbz#2348951

* Wed Feb 12 2025 Cristian Le <git@lecris.dev> - 0.10.7-3
- Various simplifications
- Added `Requires: ninja-build` by default
- Removed `Suggests` and `Recommends`, these are not likely to be used
- Removed the test conditional for epel10 since everything will be packaged
- Removed the `pyproject` subpackage since it's empty and all dependents
  are gone

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 30 2024 Packit <hello@packit.dev> - 0.10.7-1
- Update to 0.10.7 upstream release

* Wed Sep 11 2024 Packit <hello@packit.dev> - 0.10.6-1
- Update to 0.10.6 upstream release

* Wed Aug 07 2024 Packit <hello@packit.dev> - 0.10.1-1
- Update to 0.10.1 upstream release

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Cristian Le <cristian.le@mpsd.mpg.de> - 0.9.4-3
- Relax pip requirement until rawhide catches up

* Mon Jun 17 2024 Python Maint <python-maint@redhat.com> - 0.9.4-2
- Rebuilt for Python 3.13

* Tue May 14 2024 Packit <hello@packit.dev> - 0.9.4-1
- Update to 0.9.4 upstream release

* Fri Apr 19 2024 Packit <hello@packit.dev> - 0.9.0-1
- Update to 0.9.0 upstream release

* Thu Mar 28 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.8.2-2
- Produce a metapackage for the pyproject extra

* Thu Feb 29 2024 Packit <hello@packit.dev> - 0.8.2-1
- [packit] 0.8.2 upstream release

* Tue Jan 23 2024 Packit <hello@packit.dev> - 0.8.0-1
- [packit] 0.8.0 upstream release

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 08 2023 Packit <hello@packit.dev> - 0.6.1-1
- [packit] 0.6.1 upstream release

* Thu Sep 21 2023 Packit <hello@packit.dev> - 0.5.1-1
- [packit] 0.5.1 upstream release

* Tue Aug 22 2023 Cristian Le <cristian.le@mpsd.mpg.de> - 0.5.0-1
- [packit] 0.5.0 upstream release

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 05 2023 Packit <hello@packit.dev> - 0.4.4-1
- 0.4.4 upstream release

* Thu Apr 13 2023 Packit <hello@packit.dev> - 0.3.0-1
- [packit] 0.3.0 upstream release

* Fri Mar 24 2023 Miro Hrončok <miro@hroncok.cz> - 0.2.2-2
- Move the Requires, Recommends and Suggests to python3-scikit-build-core

* Mon Mar 20 2023 Cristian Le <cristian.le@mpsd.mpg.de> - 0.2.2-1
- Initial import (#2179414).