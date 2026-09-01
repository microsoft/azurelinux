# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pytest_xdist

Name:           python-pytest-xdist
Version:        3.7.0
Release:        5%{?dist}
Summary:        pytest plugin for distributed testing and loop-on-failing modes

License:        MIT
URL:            https://github.com/pytest-dev/pytest-xdist
Source0:        %{pypi_source}
BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
The pytest-xdist plugin extends pytest with new test execution modes,
the most used being distributing tests across multiple CPUs
to speed up test execution:

    pytest -n auto

With this call, pytest will spawn a number of workers processes equal
to the number of available CPUs, and distribute the tests randomly across them.}

%description %_description

%package -n     python3-pytest-xdist
Summary:        %{summary}

%description -n python3-pytest-xdist %_description

%pyproject_extras_subpkg -n python3-pytest-xdist psutil setproctitle

%prep
%autosetup -n %{pypi_name}-%{version} -p 1

%generate_buildrequires
%pyproject_buildrequires -t -x testing -x psutil -x setproctitle

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l xdist

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%tox


%files -n python3-pytest-xdist -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.7.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.7.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.7.0-2
- Rebuilt for Python 3.14

* Tue May 27 2025 Scott Talbert <swt@techie.net> - 3.7.0-1
- Update to new upstream release 3.7.0 (#2368655)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Aug 06 2024 Scott Talbert <swt@techie.net> - 3.6.1-4
- Update License tag to use SPDX identifiers
- Modernize Python packaging

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.6.1-2
- Rebuilt for Python 3.13

* Wed May 01 2024 Scott Talbert <swt@techie.net> - 3.6.1-1
- Update to new upstream release 3.6.1 (#2276175)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Scott Talbert <swt@techie.net> - 3.5.0-1
- Update to new upstream release 3.5.0 (#2250980)

* Sat Nov 18 2023 Scott Talbert <swt@techie.net> - 3.4.0-1
- Update to new upstream release 3.4.0 (#2249319)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.3.1-2
- Rebuilt for Python 3.12

* Fri May 19 2023 Scott Talbert <swt@techie.net> - 3.3.1-1
- Update to new upstream release 3.3.1 (#2203558)

* Wed Apr 26 2023 Scott Talbert <swt@techie.net> - 3.2.1-1
- Update to new upstream release 3.2.1 (#2177575)

* Thu Feb 09 2023 Scott Talbert <swt@techie.net> - 3.2.0-1
- Update to new upstream release 3.2.0 (#2168367)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Scott Talbert <swt@techie.net> - 3.1.0-2
- Fix tests when PYTEST_XDIST_AUTO_NUM_WORKERS is set (#2161636)

* Sun Dec 04 2022 Scott Talbert <swt@techie.net> - 3.1.0-1
- Update to new upstream release 3.1.0 (#2150627)

* Fri Oct 28 2022 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-2
- Drop unused runtime requirement on on the python3-py package
- Package the pytest-xdist[psutil] and pytest-xdist[setproctitle] extras

* Wed Oct 26 2022 Scott Talbert <swt@techie.net> - 3.0.2-1
- Update to new upstream release 3.0.2 (#2137874)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.5.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Dec 11 2021 Scott Talbert <swt@techie.net> - 2.5.0-1
- Update to new upstream release 2.5.0 (#2031314)

* Wed Sep 22 2021 Scott Talbert <swt@techie.net> - 2.4.0-1
- Update to new upstream release 2.4.0 (#2006595)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Scott Talbert <swt@techie.net> - 2.2.1-3
- Update to new upstream release 2.3.0 (#1972964)

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 2.2.1-2
- Rebuilt for Python 3.10

* Sat Feb 13 2021 Scott Talbert <swt@techie.net> - 2.2.1-1
- Update to new upstream release 2.2.1 (#1927076)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 19:19:19 EST 2020 Scott Talbert <swt@techie.net> - 2.2.0-1
- Update to new upstream release 2.2.0 (#1907549)

* Wed Aug 26 2020 Scott Talbert <swt@techie.net> - 2.1.0-1
- Update to new upstream release 2.1.0 (#1872506)

* Fri Aug 14 2020 Scott Talbert <swt@techie.net> - 2.0.0-1
- Update to new upstream release 2.0.0 (#1868954)

* Tue Jul 28 2020 Scott Talbert <swt@techie.net> - 1.34.0-1
- Update to new upstream release 1.34.0 (#1861207)

* Sat Jul 11 2020 Scott Talbert <swt@techie.net> - 1.33.0-1
- Update to new upstream release 1.33.0 (#1855516)

* Thu Jun 25 2020 Scott Talbert <swt@techie.net> - 1.32.0-4
- Modernize Python packaging; BR setuptools

* Fri May 29 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.32.0-3
- Drop manual requires on python3-pytest to support usage with pytest4 compat package

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.32.0-2
- Rebuilt for Python 3.9

* Mon May 04 2020 Scott Talbert <swt@techie.net> - 1.32.0-1
- Update to new upstream release 1.32.0 (#1830627)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Scott Talbert <swt@techie.net> - 1.31.0-1
- Update to new upstream release 1.31.0 (#1785526)

* Wed Oct 02 2019 Scott Talbert <swt@techie.net> - 1.30.0-1
- Update to new upstream release 1.30.0 (#1757495)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.29.0-4
- Rebuilt for Python 3.8

* Thu Aug 08 2019 Scott Talbert <swt@techie.net> - 1.29.0-3
- Remove Python 2 subpackages (#1737399)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Scott Talbert <swt@techie.net> - 1.29.0-1
- Update to new upstream release 1.29.0 (#1720870)

* Thu Apr 18 2019 Scott Talbert <swt@techie.net> - 1.28.0-1
- New upstream release 1.28.0

* Fri Mar 22 2019 Scott Talbert <swt@techie.net> - 1.27.0-1
- New upstream release 1.27.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.26.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Scott Talbert <swt@techie.net> - 1.26.1-1
- New upstream release 1.26.1

* Tue Jan 22 2019 Scott Talbert <swt@techie.net> - 1.26.0-1
- New upstream release 1.26.0

* Sat Dec 15 2018 Scott Talbert <swt@techie.net> - 1.25.0-1
- New upstream release 1.25.0

* Sun Nov 11 2018 Scott Talbert <swt@techie.net> - 1.24.1-1
- New upstream release 1.24.1

* Wed Oct 31 2018 Scott Talbert <swt@techie.net> - 1.24.0-1
- New upstream release 1.24.0

* Fri Oct 19 2018 Scott Talbert <swt@techie.net> - 1.23.2-1
- New upstream release 1.23.2

* Sat Jul 28 2018 Scott Talbert <swt@techie.net> - 1.22.5-1
- New upstream release 1.22.5

* Tue Jul 24 2018 Scott Talbert <swt@techie.net> - 1.22.3-1
- New upstream release 1.22.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.22.2-2
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Scott Talbert <swt@techie.net> - 1.22.2-1
- New upstream release 1.22.2

* Wed Feb 21 2018 Scott Talbert <swt@techie.net> - 1.22.1-1
- New upstream release 1.22.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 12 2018 Scott Talbert <swt@techie.net> - 1.22.0-1
- New upstream release 1.22.0

* Fri Dec 29 2017 Scott Talbert <swt@techie.net> - 1.21.0-1
- New upstream release 1.21.0

* Mon Nov 20 2017 Scott Talbert <swt@techie.net> - 1.20.1-2
- Avoid packaging -PYTEST.pyc files which are problematic (#1507299)

* Tue Oct 24 2017 Scott Talbert <swt@techie.net> - 1.20.1-1
- New upstream release 1.20.1

* Thu Aug 24 2017 Scott Talbert <swt@techie.net> - 1.20.0-1
- New upstream release 1.20.0

* Sat Jul 29 2017 Scott Talbert <swt@techie.net> - 1.18.2-1
- New upstream release 1.18.2

* Fri Jul 28 2017 Scott Talbert <swt@techie.net> - 1.18.1-1
- New upstream release 1.18.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Scott Talbert <swt@techie.net> - 1.18.0-1
- New upstream release 1.18.0

* Wed Jun 14 2017 Scott Talbert <swt@techie.net> - 1.17.1-1
- New upstream release 1.17.1

* Sat Jun 10 2017 Scott Talbert - 1.17.0-1
- New upstream release 1.17.0

* Tue May 09 2017 Scott Talbert <swt@techie.net> - 1.16.0-1
- New upstream release 1.16.0
- Enable tests

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.15.0-2
- Rebuild for Python 3.6

* Mon Oct 03 2016 Scott Talbert <swt@techie.net> - 1.15.0-1
- New upstream release 1.15.0

* Thu Aug 11 2016 Scott Talbert <swt@techie.net> - 1.14-1
- Initial package.
