%global srcname entrypoints
%global sum Discover and load entry points from installed packages

Name:		python-%{srcname}

# WARNING: Check if an update does not break flake8!
Version:	0.4
Release:	5%{?dist}
Summary:	%{sum}
# SPDX
License:	MIT

URL:		https://entrypoints.readthedocs.io/
Source0:	https://github.com/takluyver/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires: make
BuildRequires:	python3-devel
BuildRequires:	python3-sphinx

%description
Entry points are a way for Python packages to advertise objects with some
common interface. The most common examples are console_scripts entry points,
which define shell commands by identifying a Python function to run.

The entrypoints module contains functions to find and load entry points.

%package -n python3-%{srcname}
Summary:	%{sum}

%description -n python3-%{srcname}
Entry points are a way for Python packages to advertise objects with some
common interface. The most common examples are console_scripts entry points,
which define shell commands by identifying a Python function to run.

The entrypoints module contains functions to find and load entry points.

%package -n python-%{srcname}-doc
Summary:	Documentation for python-entrypoints

%description -n python-%{srcname}-doc
Documentation files for python-entrypoints

%prep
%autosetup -n %{srcname}-%{version} -p1


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

pushd doc
make html PYTHON="%{__python3}" SPHINXBUILD=sphinx-build-%{python3_version}
rm _build/html/.buildinfo
popd


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%pyproject_check_import


%files -n python3-%{srcname} -f %{pyproject_files}
%doc doc/_build/html
%license LICENSE

%files -n python-%{srcname}-doc
%doc doc/_build/html
%license LICENSE


%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.4-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 16 2023 Lumír Balhar <lbalhar@redhat.com> - 0.4-1
- Update to 0.4 (rhbz#2049921)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.3-17
- Rebuilt for Python 3.12

* Mon May 15 2023 Miro Hrončok <mhroncok@redhat.com> - 0.3-16
- Use flit-core to build this package, instead of flit

* Mon Feb 13 2023 Miro Hrončok <mhroncok@redhat.com>
- Convert to pyproject-rpm-macros
- The INSTALLER file now says "rpm" instead of "pip"
- Run basic import check during the build

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3-12
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 26 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3-1
- Update to 0.3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Nov 28 2018 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.3-10
- Drop py2 sub-packages

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-8
- Add missing dependency on python2-configparser (#1598998)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-7
- Fix flit invocation

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.3-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan 03 2018 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 0.2.3-3
- Restore dist-info information (#1530098).

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Michal Cyprian <mcyprian@redhat.com> - 0.2.2-6
- Use python install wheel macros

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-5
- Rebuild for Python 3.6

* Sun Nov 06 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.2-4
- Do not own pycache dir

* Mon Oct 03 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.2-3
- Consolidate two doc subpackages into one

* Sun Oct 02 2016 Mukundan Ragavan <nonamedotc@fedoraproject.org> - 0.2.2-2
- Add -doc subpackages
- Fix source url
- Add license clarification issue URL for reference

* Sat Jul 2 2016 Elliott Sales de Andrade <quantum.analyst@gmail.com> 0.2.2-1
- Initial RPM release
