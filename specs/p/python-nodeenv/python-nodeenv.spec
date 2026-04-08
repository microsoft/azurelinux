## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-nodeenv
Version:        1.10.0
Release:        %autorelease
Summary:        Node.js virtual environment builder

License:        BSD-3-Clause
URL:            https://github.com/ekalinin/nodeenv
# The PyPI sdist does not contain tests, so we use the GitHub archive
Source:         %{url}/archive/%{version}/nodeenv-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

BuildRequires:  help2man

# We don’t use tox, because we would have to patch out linting and coverage
# analysis from tox.ini, and the rest of the dependencies in
# requirements-dev.txt are all for linting and coverage—except pytest, which we
# handle manually, because this is easier than filtering the requirements file.
#
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
BuildRequires:  python3dist(pytest)
# For integration tests:
BuildRequires:  /usr/bin/node

%global _description %{expand:
nodeenv (node.js virtual environment) is a tool to create isolated node.js
environments.

It creates an environment that has its own installation directories, that
doesn’t share libraries with other node.js virtual environments.

Also the new environment can be integrated with the environment which was built
by virtualenv (python).}

%description %{_description}


%package -n python3-nodeenv
Summary:        %{summary}

%description -n python3-nodeenv %{_description}


%prep
%autosetup -n nodeenv-%{version} -p1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_linters
sed -r -i "s@'coverage', 'run', '-p',@'%{python3}',@" tests/nodeenv_test.py

# Remove unwanted shebangs from files that will not have the executable bit set
sed -r -i '1{/^#!/d}' nodeenv.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l nodeenv

# Generate the man page here, rather than in %%build, so that the executable
# script entry point is readily available.
install -d '%{buildroot}%{_mandir}/man1'
PYTHONPATH='%{buildroot}%{python3_sitelib}' \
    help2man --no-info --output='%{buildroot}%{_mandir}/man1/nodeenv.1' \
    '%{buildroot}%{_bindir}/nodeenv'


%check
# Requires network access:
k="${k-}${k+ and }not test_smoke"

%pytest -k "${k-}" -v


%files -n python3-nodeenv -f %{pyproject_files}
%doc README.rst
%doc README.ru.rst
%doc CHANGES

%{_bindir}/nodeenv
%{_mandir}/man1/nodeenv.1*


%changelog
* Thu Dec 25 2025 Tim Semeijn <fedora@semops.nl> - 1.10.0-1
- Update to version 1.10.0 (RHBZ#2424115)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.9.1-8
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.9.1-7
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.9.1-5
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.9.1-2
- Rebuilt for Python 3.13

* Thu Jun 06 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.1-1
- Update to 1.9.1 (close RHBZ#2290657)

* Sat Jun 01 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.9.0-1
- Update to 1.9.0 (close RHBZ#2283715)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.0-4
- Assert that the .dist-info directory contains a license file

* Mon Oct 23 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.8.0-3
- Replace usage of deprecated/removed pipes module (fix RHBZ#2245654)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 13 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 1.7.0-1
- Update to 1.8.0 (close RHBZ#1466314)
- Update License to SPDX
- Port to pyproject-rpm-macros (new Python guidelines)
- Package additional text documentation files
- Remove dependency on deprecated python-mock package
- Add a man page, generated with help2man

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.13.6-29
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.13.6-26
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.13.6-23
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.13.6-20
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.6-18
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.6-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.13.6-14
- Subpackage python2-nodeenv has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.6-12
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.6-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.13.6-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.6-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov  9 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 0.13.6-3
- Fix script mistakenly being included in both the python2 and python3 version
  of the package.

* Wed Sep 30 2015 Chandan Kumar <chkumar246@gmail.com> - 0.13.6-2
- Fixed files duplication

* Tue Sep 29 2015 Chandan Kumar <chkumar246@gmail.com> - 0.13.6-1
- Added python2 and python3 subpackge

* Wed Aug 12 2015 chandankumar <chkumar246@gmail.com> - 0.13.3-1
- Initial package.
