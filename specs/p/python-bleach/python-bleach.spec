# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname bleach

Name:           python-%{modname}
Version:        6.2.0
Release:        7%{?dist}
Summary:        An easy whitelist-based HTML-sanitizing tool

License:        Apache-2.0
URL:            https://github.com/mozilla/bleach
Source0:        https://files.pythonhosted.org/packages/source/b/%{modname}/%{modname}-%{version}.tar.gz

# As a result of fixed CVE-2023-24329, urllib.parse.urlsplit() now strips
# the leading C0 control and space characters.
# This breaks tests which expect those leading whitespace characters.
# Upstream vendors an ancient parse.py from Python 3.6.14 and doesn't
# experience this issue.
# Discussed upstream: https://github.com/mozilla/bleach/issues/707
Patch:          Strip-leading-whitespaces-from-expected-values.patch

BuildArch:      noarch

%global _description \
Bleach is an HTML sanitizing library that escapes or strips markup and\
attributes based on a white list.

%description %{_description}


%package -n python3-%{modname}
Summary:        An easy whitelist-based HTML-sanitizing tool
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
BuildRequires:  python3-html5lib
Requires:       python3-html5lib

%description -n python3-%{modname}
%{_description}

Python 3 version.


%pyproject_extras_subpkg -n python3-%{modname} css

%prep
%autosetup -n %{modname}-%{version} -p1

# Remove pregenerated egg-info
rm -rf bleach.egg-info

# Remove vendored libraries which were added for https://github.com/mozilla/bleach/issues/386
rm -r bleach/_vendor/
# Bleach has a shim layer that references the vendored html5lib and urllib.parse we just deleted.
# Let's patch up the imports to use the real html5lib and urllib.parse.
sed -i "s/bleach._vendor.html5lib/html5lib/g" bleach/html5lib_shim.py tests/test_clean.py
sed -i "s/bleach._vendor.parse/urllib.parse/g" bleach/parse_shim.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{modname}

%check
! find %{buildroot}%{python3_sitelib}/bleach/ -type d | grep vendor

if [ $? -ne 0 ]; then
    echo "Detected vendored libraries; please remove them."
    /usr/bin/false
fi;

%pytest -k 'not test_uri_value_allowed_protocols and not test_css_parsing_gauntlet_regex_backtracking'


%files -n python3-%{modname} -f %{pyproject_files}
%license LICENSE
%doc README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.2.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 6.2.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 6.2.0-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Jan 06 2025 Lumír Balhar <lbalhar@redhat.com> - 6.2.0-2
- Provide css extra subpackage

* Thu Nov 14 2024 Michel Lind <salimma@fedoraproject.org> - 6.2.0-1
- new version

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.1.0-2
- Rebuilt for Python 3.13

* Sun Feb 04 2024 Michel Lind <salimma@fedoraproject.org> - 6.1.0-1
- Update to 6.1.0
- Use SPDX license identifier

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Karolina Surma <ksurma@redhat.com> - 6.0.0-3
- Adjust the tests to work with the new urllib.parse.urlsplit() behavior

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 6.0.0-2
- Rebuilt for Python 3.12

* Wed Feb 08 2023 Sandro Mani <manisandro@gmail.com> - 6.0.0-1
- Update to 6.0.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 09 2021 Matthias Runge <mrunge@redhat.com> - 4.0.0-1
- update to 4.0.0 (rhbz#1923781)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.2.3-2
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Matthias Runge <mrunge@redhat.com> - 3.2.3-1
- rebase to 3.2.3 (rhbz#1918556)

* Mon Oct 05 2020 Matthias Runge <mrunge@redhat.com> - 3.2.1-1
- update to 3.2.1 (rhbz#1829635)
- fix ftbfs (1863709)
- fix CVE-2020-6816 (rhbz#1827493)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.1.4-3
- Rebuilt for Python 3.9

* Wed Apr 22 2020 Nils Philippsen <nils@redhat.com> - 3.1.4-2
- skip failing tests regardless of Python version

* Wed Apr 22 2020 Nils Philippsen <nils@redhat.com> - 3.1.4-1
- version 3.1.4
- use pythonhosted.org source URL as the tarballs match published hashes
- only skip failing tests and only on Python 3.9
- cope with html5lib prerelease on EL8

* Wed Feb 19 2020 Matthias Runge <mrunge@redhat.com> - 3.1.0-5
- skip tests for python 3.9 

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.1.0-4
- Drop python2-bleach (#1746757).

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 06 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.1.0-1
- Update to 3.1.0.
- https://github.com/mozilla/bleach/blob/v3.1.0/CHANGES

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 3.0.2-1
- Update to 3.0.2 (#1641626).
- https://github.com/mozilla/bleach/blob/v3.0.2/CHANGES

* Wed Dec 05 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4.
- https://github.com/mozilla/bleach/blob/v2.1.4/CHANGES

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.1.3-2
- Rebuilt for Python 3.7

* Tue Mar 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
