%global pypi_name pytest-timeout

Name:           python-pytest-timeout
Version:        2.3.1
Release:        4%{?dist}
Summary:        py.test plugin to abort hanging tests

# SPDX
License:        MIT
URL:            https://github.com/pytest-dev/pytest-timeout
Source0:        %{pypi_source}

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
This is a plugin which will terminate tests after a certain timeout. When doing
so it will show a stack dump of all threads running at the time. This is useful
when running tests under a continuous integration server or simply if you don’t
know why the test suite hangs.}

%description %_description

%package -n     python3-pytest-timeout
Summary:        %{summary}

%description -n python3-pytest-timeout %_description

%prep
%autosetup -p1 -n pytest-timeout-%{version}
# python-ipdb FTBFS currently
sed -i -e '/\s*ipdb$/d' tox.ini

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l pytest_timeout

%check
%tox


%files -n python3-pytest-timeout -f %{pyproject_files}
%doc README.rst

%changelog
* Tue Aug 06 2024 Scott Talbert <swt@techie.net> - 2.3.1-4
- Update License tag to use SPDX identifiers
- Modernize Python packaging

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.3.1-2
- Rebuilt for Python 3.13

* Fri Mar 08 2024 Scott Talbert <swt@techie.net> - 2.3.1-1
- Update to new upstream release 2.3.1 (#2268509)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 09 2023 Scott Talbert <swt@techie.net> - 2.2.0-1
- Update to new upstream release 2.2.0 (#2242718)
- Modernize Python packaging

* Tue Aug 08 2023 Karolina Surma <ksurma@redhat.com> - 2.1.0-7
- Declare license as an SPDX expression

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.1.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.11

* Sat Jan 22 2022 Scott Talbert <swt@techie.net> - 2.1.0-1
- Update to new upstream release 2.1.0 (#2042161)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Scott Talbert <swt@techie.net> - 2.0.2-1
- Update to new upstream release 2.0.2 (#2032002)

* Mon Oct 11 2021 Scott Talbert <swt@techie.net> - 2.0.1-1
- Update to new upstream release 2.0.1 (#2013023)

* Mon Oct 11 2021 Scott Talbert <swt@techie.net> - 2.0.0-1
- Update to new upstream release 2.0.0 (#2012634)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.4.2-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 15 2020 Scott Talbert <swt@techie.net> - 1.4.2-1
- Update to new upstream release 1.4.2 (#1857421)

* Fri Jun 26 2020 Scott Talbert <swt@techie.net> - 1.4.1-2
- Add missing BR for setuptools

* Tue Jun 16 2020 Scott Talbert <swt@techie.net> - 1.4.1-1
- Update to new upstream release 1.4.1 (#1846923)
- Modernize packaging

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.4-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Scott Talbert <swt@techie.net> - 1.3.4-1
- Update to new upstream release (#1788278)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.3-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.3-6
- Rebuilt for Python 3.8

* Thu Aug 08 2019 Scott Talbert <swt@techie.net> - 1.3.3-5
- Remove Python 2 subpackages (#1737398)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.3-3
- Add upstream patch for pytest 4 compatibility

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Scott Talbert <swt@techie.net> - 1.3.3-1
- New upstream release 1.3.3

* Tue Oct 23 2018 Scott Talbert <swt@techie.net> - 1.3.2-1
- New upstream release 1.3.2

* Fri Sep 14 2018 Scott Talbert <swt@techie.net> - 1.3.1-2
- Disable writing bytecode when running tests to avoid packaging pycache files

* Tue Jul 24 2018 Scott Talbert <swt@techie.net> - 1.3.1-1
- New upstream release 1.3.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Scott Talbert <swt@techie.net> - 1.3.0-1
- New upstream release 1.3.0

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-2
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Scott Talbert <swt@techie.net> - 1.2.1-1
- New upstream release 1.2.1 (fixes FTBFS #1590256)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jul 28 2017 Scott Talbert <swt@techie.net> - 1.2.0-3
- Updated to use versioned dependency name

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 10 2017 Scott Talbert <swt@techie.net> - 1.2.0-1
- New upstream release 1.2.0
- Enable tests

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 1.0.0-2
- Rebuild for Python 3.6

* Thu Aug 11 2016 Scott Talbert <swt@techie.net> - 1.0.0-1
- Initial package.
