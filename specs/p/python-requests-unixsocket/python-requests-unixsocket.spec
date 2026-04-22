# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name requests_unixsocket2
%global package_name requests-unixsocket

# pypi:requests-unixsocket is nolonger maintained upstream
# pypi:requests-unixsocket2 is a for that provides requests-unixsocket
# This package pulls from requests-unixsocket2 and packages as requests-unixsocket
# See change log 0.4.0-1 for details.

Name:           python-%{package_name}
Version:        0.4.0
Release: 14%{?dist}
Summary:        Use requests to talk HTTP via a UNIX domain socket

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/thelabnyc/requests-unixsocket2
Source0:        %{pypi_source}
BuildArch:      noarch

%description
%{summary}.

%package -n     python3-%{package_name}
Summary:        Use requests to talk HTTP via a UNIX domain socket

BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(waitress)

%description -n python3-%{package_name}
%{summary}.

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove shebangs
sed -i '1d' requests_unixsocket/tests/test_requests_unixsocket.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
mv %{buildroot}%{python3_sitelib}/requests_unixsocket2-%{version}.dist-info %{buildroot}%{python3_sitelib}/requests_unixsocket-%{version}.dist-info
sed -i 's/unixsocket2/unixsocket/g' %{buildroot}%{python3_sitelib}/requests_unixsocket-%{version}.dist-info/METADATA

%check
%pytest

%files -n python3-%{package_name}
%doc README.md
%license LICENSE
%{python3_sitelib}/requests_unixsocket
%{python3_sitelib}/requests_unixsocket-%{version}.dist-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.4.0-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.4.0-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.4.0-10
- Rebuilt for Python 3.14

* Fri Apr 04 2025 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-9
- Don't try to generate build dependencies by tox, there is no tox configuration
- Fixes: rhbz#2354121

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 07 2024 Dan Radez <dradez@redhat.com> - 0.4.0-7
- generate build requires

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 0.4.0-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.4.0-4
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-3
- Do not needlessly BuildRequire poetry, this package uses poetry-core

* Mon Jun 03 2024 Dan Radez <dradez@redhat.com> - 0.4.0-1
- RHBZ#2284361
  Updating to new upstream project, see comment at
  https://github.com/msabramo/requests-unixsocket/issues/73#issuecomment-2125848213
  Dated: May 22, 2024

  FYI to all: since this project seems to be abandoned, but its longevity is important to my team,
  we've forked the project as requests-unixsocket2. It should be a drop in replacement for this package.

  PyPI: https://pypi.org/project/requests-unixsocket2/0.4.0/
  Repository: https://gitlab.com/thelabnyc/requests-unixsocket2
  We've migrated the fix for this issue there, merged it, and released to PyPI as part of v0.4.0.
- Updated to pyproject macros

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.2.0-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.0-4
- Rebuilt for Python 3.11

* Tue Feb 08 2022 Dan Radez <dradez@redhat.com> - 0.2.0-3
- Don't remove egginfo

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Dan Radez <dradez@redhat.com> - 0.2.0-1
- update to 0.2.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.1.5-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.1.5-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 2 2019 Dan Radez <dradez@redhat.com> - 0.1.5-2
- Updates to initial package to address review comments
* Tue Mar  8 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.1.5-1
- Initial package.
