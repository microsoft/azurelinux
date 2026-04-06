# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sip

Name:           sip6
Version:        6.15.1
Release:        1%{?dist}
Summary:        SIP - Python/C++ Bindings Generator
%py_provides    python3-sip6

License:        BSD-2-Clause
URL:            https://github.com/Python-SIP/sip
Source0:        %{url}/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

# For tests
BuildRequires:  gcc-c++

%global _description %{expand:
SIP is a collection of tools that makes it very easy to create Python bindings
for C and C++ libraries.  It was originally developed in 1998 to create PyQt,
the Python bindings for the Qt toolkit, but can be used to create bindings for
any C or C++ library.  For example it is also used to generate wxPython, the
Python bindings for wxWidgets.}

%description %_description

%prep
%autosetup -n %{pypi_name}-%{version} -p 1

%generate_buildrequires
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install

#check
#{py3_test_envvars} {python3} -m unittest discover -v -s test


%files
%doc README.md
%license LICENSE
%{_bindir}/sip*
%{python3_sitelib}/sip-*
%{python3_sitelib}/sipbuild/

%changelog
* Thu Jan 29 2026 Jan Grulich <jgrulich@redhat.com> - 6.15.1-1
- 6.15.1

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 6.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Nov 05 2025 Jan Grulich <jgrulich@redhat.com> - 6.14.0-1
- 6.14.0

* Mon Oct 13 2025 Jan Grulich <jgrulich@redhat.com> - 6.13.1-1
- 6.13.1

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.12.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.12.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jun 08 2025 Python Maint <python-maint@redhat.com> - 6.12.0-2
- Rebuilt for Python 3.14

* Sat Jun 07 2025 Jan Grulich <jgrulich@redhat.com> - 6.12.0-1
- 6.12.0

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 6.10.0-2
- Rebuilt for Python 3.14

* Wed Feb 19 2025 Scott Talbert <swt@techie.net> - 6.10.0-1
- Update to new upstream release 6.10.0 (#2343409)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 14 2024 Scott Talbert <swt@techie.net> - 6.9.1-1
- Update to new upstream release 6.9.1 (#2332001)

* Fri Dec 06 2024 Jan Grulich <jgrulich@redhat.com> - 6.9.0-1
- 6.9.0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Scott Talbert <swt@techie.net> - 6.8.6-1
- Update to new upstream release 6.8.6 (#2293663)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.8.3-3
- Rebuilt for Python 3.13

* Thu Mar 14 2024 Miro Hrončok <mhroncok@redhat.com> - 6.8.3-2
- Workaround hang/OOM kill in Python 3.13

* Wed Feb 21 2024 Scott Talbert <swt@techie.net> - 6.8.3-1
- Update to new upstream release 6.8.3 (#2263494)

* Mon Feb 12 2024 Jan Grulich <jgrulich@redhat.com> - 6.8.2-2
- Rebuild (fixed SPDX license)

* Thu Jan 25 2024 Scott Talbert <swt@techie.net> - 6.8.2-1
- Update to new upstream release 6.8.2 (#2252260)

* Mon Oct 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.7.12-1
- 6.7.12

* Wed Aug 02 2023 Scott Talbert <swt@techie.net> - 6.7.11-1
- Update to new upstream release 6.7.11 (#2225117)

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 6.7.9-2
- Rebuilt for Python 3.12

* Wed Apr 26 2023 Scott Talbert <swt@techie.net> - 6.7.9-1
- Update to new upstream release 6.7.9 (#2185559)

* Tue Feb 07 2023 Scott Talbert <swt@techie.net> - 6.7.7-1
- Update to new upstream release 6.7.7 (#2167385)

* Tue Jan 31 2023 Scott Talbert <swt@techie.net> - 6.7.6-1
- Update to new upstream release 6.7.6 (#2165207)
- Modernize python packaging

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Scott Talbert <swt@techie.net> - 6.7.5-1
- Update to new upstream release 6.7.5 (#2131647)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Scott Talbert <swt@techie.net> - 6.6.2-1
- Update to new upstream release 6.6.2 (#2074712)

* Wed Jun 15 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 6.5.1-3
- Add patch for Python 3.11 compatibility

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 6.5.1-2
- Rebuilt for Python 3.11

* Fri Feb 18 2022 Scott Talbert <swt@techie.net> - 6.5.1-1
- Update to new upstream release 6.5.1 (#2049172)

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 14 2021 Scott Talbert <swt@techie.net> - 6.5.0-1
- Update to new upstream release 6.5.0 (#2028405)

* Sat Oct 30 2021 Scott Talbert <swt@techie.net> - 6.4.0-1
- Update to new upstream release 6.4.0 (#2018175)

* Wed Oct 13 2021 Scott Talbert <swt@techie.net> - 6.3.1-1
- Update to new upstream release 6.3.1 (#2013781)

* Tue Oct 12 2021 Scott Talbert <swt@techie.net> - 6.3.0-1
- Update to new upstream release 6.3.0 (#2013274)

* Mon Oct 04 2021 Scott Talbert <swt@techie.net> - 6.2.0-1
- Update to new upstream release 6.2.0 (#2010059)

* Wed Aug 04 2021 Scott Talbert <swt@techie.net> - 6.1.1-3
- Fix handling of Unicode docstrings

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Scott Talbert <swt@techie.net> - 6.1.1-1
- Initial package.
