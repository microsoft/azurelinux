# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sum docutils-compatibility bridge to CommonMark
%global desc A docutils-compatibility bridge to CommonMark.\
\
This allows you to write CommonMark inside of Docutils & Sphinx projects.\
\
Documentation is available on Read the Docs: http://recommonmark.readthedocs.org

Name:           python-recommonmark
Version:        0.7.1
Release:        16.git%{?dist}
Summary:        %{sum}

License:        MIT
URL:            https://github.com/readthedocs/recommonmark
Source0:        https://github.com/readthedocs/recommonmark/archive/%{version}/recommonmark-%{version}.tar.gz
BuildArch:      noarch

%description
%{desc}


%package -n     python%{python3_pkgversion}-recommonmark
Summary:        %{sum}
BuildArch:      noarch
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-docutils
BuildRequires:  python%{python3_pkgversion}-CommonMark
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-sphinx

%description -n python%{python3_pkgversion}-recommonmark
%{desc}


%prep
%setup -qn recommonmark-%{version}
# Remove upstream's egg-info

sed -i '1{\@^#!/usr/bin/env python@d}' recommonmark/scripts.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
#  install python3 first to have unversioned binaries for python 3
%pyproject_install
%pyproject_save_files recommonmark
pushd %{buildroot}%{_bindir}  # Enter buildroot bindir to ease symlink creation
for cm2bin in cm2*; do
    mv "${cm2bin}" "${cm2bin}-%{python3_version}"
    ln -s "${cm2bin}-%{python3_version}" "${cm2bin}-3"
done
popd  # Leave buildroot bindir



%check
%pyproject_check_import

# Skip some tests because of https://github.com/readthedocs/recommonmark/issues/164
%pytest --ignore tests/test_sphinx.py


%files -n python%{python3_pkgversion}-recommonmark -f %{pyproject_files}
%doc README.md
%license license.md
%{_bindir}/cm2*-3
%{_bindir}/cm2*-%{python3_version}


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.7.1-16.git
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.7.1-15.git
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-14.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Julien Enselme <jujens@jujens.eu> - 0.7.1-13.git
- Correct Python macro usages

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.7.1-12.git
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-11.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-10.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.1-9.git
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-8.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-7.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-6.git
- Run at least some tests during the build
- Remove duplicate manual runtime Requires

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 0.7.1-4.git
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Julien Enselme <jujens@jujens.eu> - 0.7.1-1
- Update to 0.7.1

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.6.0-7.git
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.6.0-4.git
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 18 2020 Julien Enselme <jujens@jujens.eu> - 0.6.0-1
- Update to 0.6.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-6.git
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-4.git
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-3.git
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2.git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Julien Enselme <jujens@jujens.eu> - 0.5.0-1
- Update to 0.5.0
- Skip some broken tests.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-19.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Julien Enselme <jujens@jujens.eu> - 0.4.0-18.gitdbed1c4
- Bump version

* Sat Oct 20 2018 Julien Enselme <jujens@jujens.eu> - 0.4.0-17.gitdbed1c4
- Fix import of commonmark
- Remove Python 2 subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-16.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-15.gitdbed1c4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-14.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.4.0-13.gitdbed1c4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-12.gitdbed1c4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 22 2017 Julien Enselme <jujens@jujens.eu> - 0.4.0-11.gitdbed1c4
- Fix requires

* Wed Feb 22 2017 Julien Enselme <jujens@jujens.eu> - 0.4.0-10.gitdbed1c4
- Add support for CommonMark 0.7.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-9.git7ca5247
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-8.git7ca5247
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-7.git7ca5247
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 11 2016 Julien Enselme - 0.4.0-6.git7ca5247
- Fix typo in comment

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5.git7ca5247
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-4.git7ca5247
- Move unversionned binaries to python2 subpackage

* Sun Jan 17 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-3.git7ca5247
- Use tarball from github to have tests and LICENSE
- Add %%check section

* Sat Jan 16 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-2
- Remove separate source tag for license
- Add binary to python2 subpackage

* Sun Jan 10 2016 Julien Enselme <jujens@jujens.eu> - 0.4.0-1
- Update to 0.4.0

* Thu Dec 31 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-2
- Add missing dist tag

* Fri Dec 4 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-1
- Inital package
